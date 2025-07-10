# 仕訳帳をGET

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
    "download_type": "generic_v2"  # これを追加することでエラーを回避
}

# 仕訳一覧を取得
response = requests.get(
    "https://api.freee.co.jp/api/1/journals",
    headers=headers,
    params=params
)

if response.status_code == 202:
    journals = response.json()
    print(journals)  # 取得した仕訳一覧を表示
else:
    print("Error:", response.json())