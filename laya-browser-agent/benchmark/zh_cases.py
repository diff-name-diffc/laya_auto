"""Built-in Chinese browser scenarios with a rule-based oracle.

The gold answer for each case is derived from jev-ultrafast's own published
next-action rules (``NEXT_ACTION``), not from subjective labelling: e.g. "fill
required fields before submitting", "submit populated search fields before
opening a result", "do not toggle a control already in the requested state".
Every case fixes one page state and one goal, so the rule determines a single
correct operation and target.

This set needs no download and exercises Chinese text, which the Mind2Web port
cannot (Mind2Web is English-only). It is small by design -- a diagnostic for
Chinese-language handling, not a statistical claim.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _el(node: int, label: str, kind: str, role: str, value: str = "") -> Dict[str, Any]:
    a = {"id": f"{kind}:{node}", "kind": kind, "label": label, "role": role, "node": node}
    if kind == "fill":
        a["value"] = value
        a["current_value"] = value
    elif kind == "select":
        # jev emits one action per <select> option; each carries its option value.
        a["value"] = value or label.rsplit(" ", 1)[-1]
        a["current_value"] = "请选择"
    return a


def _page(title: str, text: str, actions: List[Dict[str, Any]], url: str = "https://example.cn/") -> Dict[str, Any]:
    return {"url": url, "title": title, "text": text, "actions": actions}


FLIGHT_TEXT = ("携程旅行网 机票 单程 往返 多程 出发城市 到达城市 出发日期 乘客 舱位 "
               "经济舱 公务舱 头等舱 搜索航班 国内机票 国际机票 特价机票 航班动态")

FLIGHT_ACTIONS = [
    _el(1, "单程", "click", "button"),
    _el(2, "往返", "click", "button"),
    _el(3, "多程", "click", "button"),
    _el(4, "出发城市 请输入城市", "fill", "textbox", ""),
    _el(5, "到达城市 请输入城市", "fill", "textbox", ""),
    _el(6, "出发日期 请选择日期", "click", "button"),
    _el(7, "乘客人数 1成人", "click", "button"),
    _el(8, "舱位 经济舱", "select", "combobox"),
    _el(9, "搜索航班", "click", "button"),
]


def cases() -> List[Dict[str, Any]]:
    """The Chinese scenario set."""
    out: List[Dict[str, Any]] = []

    flight_goal = "搜索2026年9月20日从北京到上海的单程机票，1名成人，经济舱"
    out.append({
        "case_id": "zh-flight-empty-form",
        "source": "zh:flight",
        "goal": flight_goal,
        "page": _page("机票查询 - 携程旅行网", FLIGHT_TEXT, FLIGHT_ACTIONS),
        "history": [],
        # empty form -> the rule says fill required fields before submitting
        "gold_op": "TYPE_TEXT",
        "gold_id": "fill:4",
        "rationale": "表单为空，应先填出发城市（规则：提交前先填必填字段）",
    })
    out.append({
        "case_id": "zh-flight-from-filled",
        "source": "zh:flight",
        "goal": flight_goal,
        "page": _page("机票查询 - 携程旅行网", FLIGHT_TEXT, [
            _el(1, "单程", "click", "button"),
            _el(4, "出发城市 请输入城市", "fill", "textbox", "北京"),
            _el(5, "到达城市 请输入城市", "fill", "textbox", ""),
            _el(6, "出发日期 请选择日期", "click", "button"),
            _el(9, "搜索航班", "click", "button"),
        ]),
        "history": [{"action": "填写 出发城市", "kind": "type_text", "text": "北京", "page_changed": False}],
        "gold_op": "TYPE_TEXT",
        "gold_id": "fill:5",
        "rationale": "出发城市已填，下一个必填字段是到达城市",
    })
    out.append({
        "case_id": "zh-flight-ready-to-submit",
        "source": "zh:flight",
        "goal": flight_goal,
        "page": _page("机票查询 - 携程旅行网", FLIGHT_TEXT, [
            _el(4, "出发城市 请输入城市", "fill", "textbox", "北京"),
            _el(5, "到达城市 请输入城市", "fill", "textbox", "上海"),
            _el(6, "出发日期 请选择日期", "fill", "textbox", "2026-09-20"),
            _el(9, "搜索航班", "click", "button"),
        ]),
        "history": [
            {"action": "填写 出发城市", "kind": "type_text", "text": "北京", "page_changed": False},
            {"action": "填写 到达城市", "kind": "type_text", "text": "上海", "page_changed": False},
            {"action": "填写 出发日期", "kind": "type_text", "text": "2026-09-20", "page_changed": False},
        ],
        "gold_op": "CLICK",
        "gold_id": "click:9",
        "rationale": "字段已就绪且搜索按钮可见（规则：立即点击搜索）",
    })
    out.append({
        "case_id": "zh-flight-oneway-already-selected",
        "source": "zh:flight",
        "goal": "搜索北京到上海的单程机票",
        "page": _page("机票查询 - 携程旅行网", FLIGHT_TEXT, [
            _el(1, "单程", "click", "button"),
            _el(2, "往返", "click", "button"),
            _el(4, "出发城市 请输入城市", "fill", "textbox", ""),
        ]),
        "history": [{"action": "点击 单程", "kind": "click", "text": None, "page_changed": True}],
        # "单程" already applied -> do not re-toggle; next step is the origin field
        "gold_op": "TYPE_TEXT",
        "gold_id": "fill:4",
        "rationale": "单程已选中，不应重复切换（规则：不要重复已满足的步骤）",
    })

    out.append({
        "case_id": "zh-login-empty",
        "source": "zh:login",
        "goal": "用账号密码登录",
        "page": _page("用户登录", "用户登录 用户名 密码 记住我 登录 忘记密码 注册新账号", [
            _el(1, "用户名", "fill", "textbox", ""),
            _el(2, "密码", "fill", "textbox", ""),
            _el(3, "记住我", "click", "checkbox"),
            _el(4, "登录", "click", "button"),
            _el(5, "忘记密码", "click", "link"),
            _el(6, "注册新账号", "click", "link"),
        ]),
        "history": [],
        "gold_op": "TYPE_TEXT",
        "gold_id": "fill:1",
        "rationale": "先填用户名（规则：提交前先填必填字段）",
    })
    out.append({
        "case_id": "zh-login-ready",
        "source": "zh:login",
        "goal": "用账号密码登录",
        "page": _page("用户登录", "用户登录 用户名 密码 登录", [
            _el(1, "用户名", "fill", "textbox", "alice"),
            _el(2, "密码", "fill", "textbox", "secret123"),
            _el(4, "登录", "click", "button"),
        ]),
        "history": [
            {"action": "填写 用户名", "kind": "type_text", "text": "alice", "page_changed": False},
            {"action": "填写 密码", "kind": "type_text", "text": "secret123", "page_changed": False},
        ],
        "gold_op": "CLICK",
        "gold_id": "click:4",
        "rationale": "账号密码已填，点击登录",
    })

    out.append({
        "case_id": "zh-shop-add-to-cart",
        "source": "zh:shop",
        "goal": "把这款商品加入购物车",
        "page": _page("商品详情", "商品详情 无线蓝牙耳机 价格 299 元 加入购物车 立即购买 收藏 分享", [
            _el(1, "商品图片", "click", "img"),
            _el(2, "加入购物车", "click", "button"),
            _el(3, "立即购买", "click", "button"),
            _el(4, "收藏", "click", "button"),
            _el(5, "分享", "click", "button"),
        ]),
        "history": [],
        "gold_op": "CLICK",
        "gold_id": "click:2",
        "rationale": "目标是加入购物车，直接点击对应按钮",
    })
    out.append({
        "case_id": "zh-pagination-next",
        "source": "zh:pagination",
        "goal": "查看第二页的搜索结果",
        "page": _page("搜索结果", "搜索结果 共 120 条 上一页 1 2 3 下一页 排序方式", [
            _el(1, "上一页", "click", "link"),
            _el(2, "第1页", "click", "link"),
            _el(3, "第2页", "click", "link"),
            _el(4, "下一页", "click", "link"),
            _el(5, "排序方式", "select", "combobox"),
        ]),
        "history": [],
        "gold_op": "CLICK",
        "gold_id": "click:3",
        "rationale": "目标明确为第二页，点击页码 2（而非下一页）",
    })
    out.append({
        "case_id": "zh-search-submit-query-filled",
        "source": "zh:search",
        "goal": "搜索北京的天气",
        "page": _page("搜索", "搜索 输入关键词 北京 搜索 热门搜索 天气 新闻 地图", [
            _el(1, "搜索框", "fill", "searchbox", "北京"),
            _el(2, "搜索", "click", "button"),
            _el(3, "热门：天气", "click", "link"),
            _el(4, "热门：新闻", "click", "link"),
        ]),
        "history": [{"action": "填写 搜索框", "kind": "type_text", "text": "北京", "page_changed": False}],
        "gold_op": "CLICK",
        "gold_id": "click:2",
        "rationale": "查询已填入，应提交搜索（规则：先提交已填搜索框）",
    })
    out.append({
        "case_id": "zh-done-goal-satisfied",
        "source": "zh:done",
        "goal": "打开关于我们页面",
        "page": _page("关于我们 - 公司简介", "关于我们 公司简介 发展历程 联系我们 加入我们", [
            _el(1, "公司简介", "click", "link"),
            _el(2, "发展历程", "click", "link"),
            _el(3, "联系我们", "click", "link"),
        ], url="https://example.cn/about"),
        "history": [{"action": "点击 关于我们", "kind": "click", "text": None, "page_changed": True}],
        # already on the target page -> DONE is correct
        "gold_op": "DONE",
        "gold_id": None,
        "rationale": "目标页面已打开，目标已满足",
    })

    return out
