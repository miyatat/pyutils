# 取引一覧を取得をGET

import requests


# 事業所
ACCESS_TOKEN = ""
COMPANY_ID = ""

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

params = {
    "company_id": COMPANY_ID,
}

# 取引一覧を取得
response = requests.get(
    "https://api.freee.co.jp/api/1/deals",
    headers=headers,
    params=params
)

if response.status_code == 200:
    journals = response.json()
    print(journals)  # 取得した仕訳一覧を表示
else:
    print("Error:", response.json())