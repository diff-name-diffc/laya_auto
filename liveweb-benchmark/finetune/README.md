# LoRA/继续训练预研结论与工具包

## 结论：不走 peft-LoRA，走官方"继续训练"路径

预研了 `cklxx/laya-browser`（HF 公开仓库，训练代码在 `code/finetune/`）后确认：

1. **没有 LoRA 支持，也不需要**。v17s 自己就是"从 v15s 用官方 RLCD trainer 继续训
   1 个 epoch"的产物（`run_v17s.sh`）——继续训练就是官方认可的增量改进方式；
   其 encoder 学习率（2.5e-5 × cosine → 1e-6）本就相当于温和的增量适配。
2. **训练配方**：RLCD（noisy-logit policy gradient + soft CE），单卡，micro=4 ×
   accum=8，AdamW wd=0.01，可断点续训（resume.pt，每 300 步）。
3. **硬件**：作者在 RTX 4070 Ti 16GB 上全量训练（200k 条 1 epoch ≈ 2h）；
   `train.py` 硬编码 CUDA——本脚本已加 DEVICE=mps 补丁，Mac 上可行但更慢
   （322M 模型 + 1024 token 序列，MPS 预计慢 3-5×，2k 条 ≈ 10-20 分钟，完全可接受）。
4. **数据契约**（`build_items.py`）：case 带 `goal/history/gold_op/gold_id/source`，
   页面要么 `page`（pages.jsonl 的索引）要么内联 `page_obj`；`kind=done` 的案例
   必须带 `page_obj`；`source=dagger` 会被跳过；非 mind2web/nnetnav 源需要整型
   `page` 字段（仅用于留出划分）。**我们的 distill schema 经
   `convert_distill.py` 一比一映射即可食用**（762/762 零丢弃实测）。
   训练器自带类别均衡（DONE×4、TYPE_TEXT×3 等重复采样）——我们无需预平衡。
5. **官方数据配比参考**（v17s = 200k items）：421 爬取页 + 700 DONE 态 +
   Mind2Web 7.3k + NNetNav 8.9k + 2.3k 真实浏览轨迹 + webgym 70k。我们的
   rescue 数据本质就是他们的 "DAgger/rollout" 类——注意官方在 v15s **清掉了
   DAgger 数据**（质量顾虑），但我们的 rescue 是 VLM 教师轨迹（比自蒸馏 DAgger
   干净），且量小（几百 vs 数万），作增量补弱风险可控。

## 使用

```bash
# 烟雾验证（数据契约 + 训练器端到端，64 条 1 分钟级）：
bash finetune/run_distill.sh 1  # 前置 SMOKE=1
SMOKE=1 bash finetune/run_distill.sh

# 正式（当前数据量）：
bash finetune/run_distill.sh 1        # 1 epoch continue from v17s
```

产出 `finetune/work/laya-browser/code/out/laya-browser-v18d/`，结构与 v17s 相同，
可直接用官方 `systemone_server.py` 起服务替换我们的 `--base-url` 后端。

## 评测协议（训练后必跑，顺序固定）

1. **静态回归**（防伤基线）：laya-browser-agent 仓库的 Mind2Web 250 例
   （op 0.892 / target 0.588 为底线）；
2. **34 任务 live 套件**：与 v17s 的 56-73% 基线对照（同种子、3 轮）；
3. **救援调用率**：级联日志中 VLM_RESCUE 次数应显著下降（弱项收敛的直接证据）。

## 风险与对策

| 风险 | 对策 |
|---|---|
| 小数据继续训练灾难性遗忘 | 官方 LR 本身温和；若静态回归掉分，掺 30-50% Mind2Web 回放重跑 |
| google 首页过采样（rescue 富集处） | convert 时按 (url, gold) 去重已做；必要时按 host 降采样 |
| MPS 数值差异 | SMOKE 先验证 loss 量级与 CUDA 版一致（可后期在远程 Linux 复核）|
