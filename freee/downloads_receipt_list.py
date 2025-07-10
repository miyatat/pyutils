# 取引一覧を取得をGET
import json
import requests

# 事業所
ACCESS_TOKEN = ""
COMPANY_ID = ""
USER_NAME = ""
START_DATE = "2024-07-01"
END_DATE = "2025-07-10"

SAVE_PATH = "receipts/receipts.json"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

params = {
    "company_id": COMPANY_ID,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "user_name": USER_NAME,
    "limit": 3000 # max 3000件が仕様
}

# 取引一覧を取得
response = requests.get(
    "https://api.freee.co.jp/api/1/receipts",
    headers=headers,
    params=params
)

if response.status_code == 200:
    lists_json = response.json()
    with open(SAVE_PATH, 'w', encoding='utf-8') as f:
        json.dump(lists_json, f, ensure_ascii=False, indent=4)
    print(lists_json)  # 取得した一覧を表示
else:
    print("Error:", response.json())