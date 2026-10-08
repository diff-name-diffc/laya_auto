# liveweb-benchmark

Live-web 端到端能力基准：用 **CloakBrowser（免费锁定版）** 驱动真实浏览器，
把每一页观测成候选元素表，交给远程 `POST /v1/systemone` Laya 决策服务（浏览器微调
checkpoint），在 **Google 各类 AI 资讯搜索** 与 **GitHub 热门仓库预览调研** 两类真实
任务上测量模型的端到端能力。

实现遵循 `../laya-browser-agent/AGENT_INTEGRATION_PROMPT.md` 的设计（五层校验、DOM
主路观测、守卫式决策循环、独立验证器），并补齐参考实现缺失的部分：完整语义 marker
新鲜度校验、≤250 元素表截断（视口优先）、413 裁剪重发、状态码重试语义、挑战页
零步终止、低置信度落账。

## 快速开始

```bash
cd liveweb-benchmark
python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'

# 1) 纯逻辑单测（无浏览器、无网络）
.venv/bin/python -m pytest -q

# 2) 列出任务
.venv/bin/python -m agentbench.runner --list-tasks

# 3) 冒烟：真实浏览器 + 观测层（不调用模型）——首次运行会下载 ~200MB 免费二进制
.venv/bin/python -m agentbench.runner --dry-run google-ai-openai
.venv/bin/python -m agentbench.runner --dry-run github-trending-view

# 4) 全量基准（默认后端 http://10.144.144.2:8000，可 --base-url 覆盖）
.venv/bin/python -m agentbench.runner --base-url http://10.144.144.2:8000
#    只跑某一类 / 某几个任务：
.venv/bin/python -m agentbench.runner --source github
.venv/bin/python -m agentbench.runner --task google-ai-openai --task github-search-llm
```

报告输出到 `results/<时间戳>/report.md`（JSON 同目录）。截图加 `--shots shots/`。

## 反挑战默认姿态（均可逆）

实测 Google `/search` 结果页对无头 + 矬编码时区的组合有概率性挑战墙（首页从不变墙），
因此基准默认：

- **有头模式**（`--headless` 退回无头）；
- **热会话**（`--fresh-session` 退回每任务新浏览器）：整个 run 复用一个浏览器 +
  上下文 + 固定指纹种子（跨 run 稳定，`--fingerprint N` 指定、`--fingerprint-random`
  随机），站点看到的是有历史的连续会话而非一批陌生分身；
- **geoip 一致性**（`--no-geoip` 关闭）：locale/timezone 由实际出口 IP 解析对齐，
  不再硬编码 America/New_York 与真实出口打架；
- **careful 拟人档**（`--human-preset default` 换标准档）+ 动作间自然停顿；
- **挑战页等待自愈**（`--challenge-wait 6`，0 关闭）：Cloudflare 类 JS 挑战常会
  自行通过，先等再判死；Google `/sorry` 墙通常不消失，等待只多花几秒。

## 蒸馏数据（救援即产训）

每次运行自动产出 `results/<ts>/traindata.jsonl`，schema 与 laya 浏览器微调的训练格式一致
（`benchmark/browser_request.build_request` 直接可消费），两条来源：

- `liveweb:rescue`：**每次 VLM 救援**必然导出——卡住时的完整观测（页面+元素表）+
  教练历史（拒绝原因/空框提示）+ gold（纠正动作 op/id）。这是管线产出的最高信噪比
  数据，直接对症已测得的弱点（提前 DONE、第三步断崖、列表选择）；
- `liveweb:model-step`：仅在运行**独立验证通过**时导出该运行的全部模型步（整条
  轨迹在黄金路径上）。

用级联跑得越多，下一代微调的训练数据越多——救援本身在免费生产训练数据。

## 任务套件（28 个）

Google 任务起点固定 `?hl=en&gl=us`（消掉跟随出口 IP 的"Open 搜索"首页变体——实测该
变体直接造成 3 个失败）。按官方逐操作基准（TYPE_TEXT top-1 **1.00**、SELECT 0.80、
CLICK 0.51，中文=英文）布置了强项探针与弱项探针：

| 类别 | 任务 | 探测什么 |
|---|---|---|
| 搜索流（TYPE_TEXT 强项） | `google-ai-*` 8 个、`google-news-tab/-images-tab/-page2` | 打字→提交→（标签页/翻页） |
| 首结果选择（CLICK 弱项） | `google-wikipedia`、`github-search-first`、`github-trending-ai-repo/-first-repo` | 多近似候选中选一 |
| 判停纪律 | `github-trending-view`、`github-topic-llm`、`github-open-pytorch` | 满足页上的校准 DONE |
| 菜单/过滤导航 | `github-trending-python`、`github-search-llm` | SELECT 类比 + 对话框输入 |
| **IT/编码调研**（`google-it-*`、`github-it-http-server`） | asyncio/rust-vs-go/k8s/pydantic 搜索流 + **三個多跳探针**（stackoverflow/MDN/FastAPI 官方文档：搜索→点开目标站）+ GitHub IT 搜索 | 编码主题搜索调研，多跳打点 |

**成功 = 独立验证通过 ∧ 模型选了 DONE**，两者分开报告；验证证据全部为逐日稳定 token。

## DONE 门控（可选 VLM 旁路，默认关）

实测主要失败模式是高置信提前 DONE（元素重标注型 L2 治不了它），因此旁路第一阶段的
插入点是**终态门控**：模型选 DONE 时做一次有界 VLM 判定（截图 + goal + 页面文本 →
"所有要求是否都有可见证据"），不通过则把缺失项注入 recent_actions 让循环重决策
（最多拒绝 2 次，VLM 异常一律 fail-open，不配置端点则完全不影响主路——不变量 6）。
任何 OpenAI 兼容视觉端点可用：

```bash
.venv/bin/python -m agentbench.runner --vlm-base-url https://api.xxx.com \
    --vlm-model glm-4v-plus --vlm-api-key ...   # 启用门控
```

## 关键语义

- **元素只进 `questions.*.criteria`**，绝不进 `state`（v3 格式硬约束）。
- **门控用 `confidence`**，τ=0.35：低置信度步记录为 `low_confidence`、元素标记 dirty
  （VLM 旁路触发接口，本基准不部署 VLM，主路永不阻塞）。
- **不自动回车**：提交搜索是模型自己的决策（PRESS_ENTER / CLICK 搜索按钮）。
- **新鲜度**：URL 短路 + 语义 marker 全量重算，页面变了就丢弃决策重新观测；
  `PRESS_ENTER` 这种页级提交也做 URL 守卫（焦点假设不能跨导航泄漏，焦点本身
  不进 marker，同 URL 焦点漂移是已知残余风险）。
- **守卫**：连续 3 次无效决策、4 步无进展、3 步同目标重复、连续 4 次 stale
  （`unstable-page`）、步数/请求预算、挑战页立即终止（`bot-challenge`）。
- **413 裁剪重发**：候选表减半重发一次，且答案永远对着"产生它的那张表"解析
  （不跨表）；"同列表不同截断尺寸下索引 k 指向同一元素"的前缀不变量有回归测试钉死。
- **无效决策计数只在真正执行成功后清零**——参考实现实测踩过的两个坑之一。

## CloakBrowser 说明（免费版）

- macOS 免费二进制是 **145.0.7632.109.2**（v146 无 darwin 资产；Linux/Windows 为
  146.0.7680.177.5），按平台写死 pin，不会漂到 Pro-only 版本。
- 免登录 keyless 使用：无并发限制、不需要 GitHub key。**不要**运行 `cloakbrowser login`。
- 每任务用 task_id 派生的固定指纹种子（`--fingerprint=N`），跨 run 可比；
  `--fingerprint-random` 换随机身份。
- humanize 默认开启（`--no-humanize` 关闭）：拟人点击/输入（含打错自纠）。
  `mouse.wheel` 滚动未被 CloakBrowser 拟人化——已知限制。
- `page.wait_for_timeout` 被替换为进程内 sleep（CloakBrowser 提示该调用有可检测的
  CDP 往返）。
- macOS 首次运行若被 Gatekeeper 拦截，browser.py 会自动尝试
  `xattr -cr ~/.cloakbrowser/chromium-*/Chromium.app`。

## 网络与礼貌性

浏览器流量走本机 Surge 增强模式（TUN）直连，launch 不传代理；`--proxy` 备用。
任务串行执行，任务间默认 8s 延时（`--delay`），单 run 12 个任务——刻意保持克制的
请求率。

## 目录

```
agentbench/
├── observe.py          # L0 观测 + L1 结构信号 + 挑战页探测 + 视口优先截断
├── request_builder.py  # v3 请求格式（NEXT_ACTION/TARGET 原文；元素只进 criteria）
├── decision_client.py  # /v1/systemone：健康检查、状态码语义、500/503/网络重试
├── validators.py       # 五层校验（纯函数，可单测）
├── executor.py         # 完整新鲜度 + 输入前可见性；不自动回车
├── loop.py             # 决策循环 + 全部守卫 + StepRecord 轨迹（observe/act 可注入）
├── browser.py          # CloakBrowser 免费版 pin、指纹种子、适配
├── tasks.py            # 12 个任务定义
├── verify.py           # 独立验证器（bot 墙优先拒绝）
├── text_model.py       # 填空文本供给（只能来自任务 queries）
├── runner.py           # CLI 编排（--dry-run / --list-tasks / 全量运行）
└── report.py           # JSON + Markdown 报告
tests/                  # 脚本化假模型打穿校验层与循环守卫（无浏览器无网络）
```
