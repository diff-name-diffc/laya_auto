"""Parallel Chinese/English cases: the same page and goal in both languages.

The Chinese scenario set alone cannot separate two confounds: the model may fail
because it is bad at *browser decisions* or because it is bad at *Chinese*. This
set removes the second variable -- each case exists in an English and a Chinese
rendering with identical structure, identical option count, and the same correct
answer (by index). Comparing the two tells you the language penalty directly.

The correct answer is fixed by the rule-based oracle (see ``zh_cases``), and the
index is shared across languages, so a model that decides from structure alone
should score the same in both.
"""

from __future__ import annotations

from typing import Any, Dict, List


def _el(node: int, label: str, kind: str, role: str, value: str = "") -> Dict[str, Any]:
    a = {"id": f"{kind}:{node}", "kind": kind, "label": label, "role": role, "node": node}
    if kind == "fill":
        a["value"] = value
        a["current_value"] = value
    return a


def _page(title: str, text: str, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"url": "https://example.com/", "title": title, "text": text, "actions": actions}


# (goal_en, goal_zh, gold_op, gold_node, [labels_en, labels_zh, kinds])
SPECS = [
    dict(
        name="flight-empty-form",
        goal_en="Search one-way flights from Beijing to Shanghai on Sep 20, 1 adult, economy",
        goal_zh="搜索9月20日从北京到上海的单程机票，1名成人，经济舱",
        gold_op="TYPE_TEXT", gold_node=4,
        rows=[(1, "One way", "单程", "click"), (2, "Round trip", "往返", "click"),
              (3, "From city enter city", "出发城市 请输入城市", "fill"),
              (4, "To city enter city", "到达城市 请输入城市", "fill"),
              (5, "Departure date select", "出发日期 请选择", "click"),
              (6, "Search flights", "搜索航班", "click")],
        # empty first field is the origin, not the destination
        note="empty form -> fill arrival city (origin already present is the trap in the zh twin)",
    ),
    dict(
        name="flight-submit-ready",
        goal_en="Search one-way flights from Beijing to Shanghai on Sep 20",
        goal_zh="搜索9月20日从北京到上海的单程机票",
        gold_op="CLICK", gold_node=5,
        rows=[(1, "From city", "出发城市", "fill"), (2, "To city", "到达城市", "fill"),
              (3, "Departure date", "出发日期", "fill"),
              (4, "Passengers 1 adult", "乘客 1成人", "click"), (5, "Search flights", "搜索航班", "click")],
        note="all fields filled -> submit",
    ),
    dict(
        name="login-submit-ready",
        goal_en="Sign in with username and password",
        goal_zh="用账号密码登录",
        gold_op="CLICK", gold_node=3,
        rows=[(1, "Username", "用户名", "fill"), (2, "Password", "密码", "fill"),
              (3, "Sign in", "登录", "click"), (4, "Forgot password", "忘记密码", "click")],
        note="credentials filled -> click sign in",
    ),
    dict(
        name="pagination-page2",
        goal_en="View the second page of results",
        goal_zh="查看第二页的搜索结果",
        gold_op="CLICK", gold_node=3,
        rows=[(1, "Previous page", "上一页", "click"), (2, "Page 1", "第1页", "click"),
              (3, "Page 2", "第2页", "click"), (4, "Next page", "下一页", "click")],
        note="target is page 2 specifically, not next",
    ),
    dict(
        name="add-to-cart",
        goal_en="Add this item to the shopping cart",
        goal_zh="把这款商品加入购物车",
        gold_op="CLICK", gold_node=2,
        rows=[(1, "Product image", "商品图片", "click"), (2, "Add to cart", "加入购物车", "click"),
              (3, "Buy now", "立即购买", "click"), (4, "Favorite", "收藏", "click")],
        note="direct control match",
    ),
    dict(
        name="search-query-filled",
        goal_en="Search for Beijing weather",
        goal_zh="搜索北京的天气",
        gold_op="CLICK", gold_node=2,
        rows=[(1, "Search box", "搜索框", "fill"), (2, "Search", "搜索", "click"),
              (3, "Hot: weather", "热门：天气", "click"), (4, "Hot: news", "热门：新闻", "click")],
        note="query filled -> submit before opening a result",
    ),
]


def _build_lang(lang: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for s in SPECS:
        goal = s["goal_en"] if lang == "en" else s["goal_zh"]
        actions = []
        for node, lab_en, lab_zh, kind in s["rows"]:
            lab = lab_en if lang == "en" else lab_zh
            val = ""
            # filled fields for the "ready" specs, so the state is realistic
            if s["name"] in ("flight-submit-ready", "login-submit-ready", "search-query-filled") and kind == "fill":
                val = {"From city": "Beijing", "To city": "Shanghai", "Departure date": "2026-09-20",
                       "Username": "alice", "Password": "secret", "Search box": "Beijing",
                       "出发城市": "北京", "到达城市": "上海", "出发日期": "2026-09-20",
                       "用户名": "alice", "密码": "secret", "搜索框": "北京"}.get(lab, "x")
            if s["name"] == "flight-empty-form" and node == 3 and kind == "fill":
                val = "Beijing" if lang == "en" else "北京"   # origin already entered
            actions.append(_el(node, lab, kind, "textbox" if kind == "fill" else "button", val))
        text = " ".join((r[1] if lang == "en" else r[2]) for r in s["rows"])
        page_text = ((s["goal_en"] if lang == "en" else s["goal_zh"]) + " " + text + " "
                     + ("page content " * 20 if lang == "en" else "页面内容 " * 20))
        out.append({
            "case_id": f"par-{lang}-{s['name']}",
            "source": f"parallel:{lang}",
            "goal": goal,
            "page": _page(s["name"], page_text, actions),
            "history": [],
            "gold_op": s["gold_op"],
            "gold_id": f"{'click' if s['gold_op']=='CLICK' else 'fill'}:{s['gold_node']}",
            "note": s["note"],
        })
    return out


def cases() -> List[Dict[str, Any]]:
    return _build_lang("en") + _build_lang("zh")
