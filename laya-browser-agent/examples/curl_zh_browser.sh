#!/usr/bin/env bash
# 中文场景浏览器自动化测试
#
# 先启动服务（服务浏览器微调模型）：
#   cd inference-server && ./start.sh --browser --device mps
# 然后运行：
#   bash examples/curl_zh_browser.sh                 # 默认 127.0.0.1:8000
#   bash examples/curl_zh_browser.sh 192.168.31.188 8000
set -euo pipefail

HOST="${1:-127.0.0.1}"
PORT="${2:-8000}"
URL="http://${HOST}:${PORT}/v1/systemone"

echo "== POST ${URL} =="
curl -s "$URL" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "state": {
      "page": {
        "url": "https://www.ctrip.com/flights",
        "title": "机票查询 - 携程旅行网",
        "text": "携程旅行网 机票 单程 往返 多程 出发城市 到达城市 出发日期 乘客 舱位 经济舱 搜索航班 国内机票 国际机票"
      },
      "elements": [
        {"index": 1}, {"index": 2}, {"index": 3}, {"index": 4}, {"index": 5},
        {"index": 6}, {"index": 7}, {"index": 8}, {"index": 9}
      ],
      "recent_actions": []
    },
    "questions": {
      "operation": {
        "type": "choice",
        "instructions": {"goal": "搜索2026年9月20日从北京到上海的单程机票，1名成人，经济舱",
                         "rules": "基于当前页面，用一步操作推进整个目标。"},
        "criteria": {
          "CLICK": "点击元素、按钮、菜单项或建议选项。",
          "TYPE_TEXT": "在可编辑输入框中输入或替换文本。",
          "SELECT": "选择一个已观察到的下拉选项。",
          "DONE": "所有要求都已可见地满足。",
          "BLOCKED": "没有支持的操作可以继续推进。"
        }
      },
      "click_target": {
        "type": "choice",
        "instructions": {"goal": "搜索2026年9月20日从北京到上海的单程机票，1名成人，经济舱",
                         "operation": "CLICK"},
        "criteria": {
          "1": "单程", "2": "往返", "3": "多程",
          "4": "出发城市 请输入城市", "5": "到达城市 请输入城市",
          "6": "出发日期 请选择日期", "7": "乘客人数 1成人",
          "8": "舱位 经济舱", "9": "搜索航班"
        }
      },
      "type_text_target": {
        "type": "choice",
        "instructions": {"goal": "搜索2026年9月20日从北京到上海的单程机票，1名成人，经济舱",
                         "operation": "TYPE_TEXT"},
        "criteria": {
          "4": "出发城市 请输入城市",
          "5": "到达城市 请输入城市"
        }
      }
    }
  }' | python3 -m json.tool
