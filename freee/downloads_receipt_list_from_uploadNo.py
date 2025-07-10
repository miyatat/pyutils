# 取引一覧を取得をGET
import csv
import requests
import json

# 事業所
ACCESS_TOKEN = ""
COMPANY_ID = ""
USER_NAME = ""
START_DATE = "2024-07-01"
END_DATE = "2025-07-10"

SAVE_PATH = "receipts_B級/receipts.csv"

UPLOAD_NUMBERLIST = [

]

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

receipt_id_list = []

for upload_number in UPLOAD_NUMBERLIST:

    params = {
        "company_id": COMPANY_ID,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "user_name": USER_NAME,
        "number" : upload_number,
        "limit": 3000 # max 3000件が仕様
    }

    # 取引一覧を取得
    response = requests.get(
        "https://api.freee.co.jp/api/1/receipts",
        headers=headers,
        params=params
    )

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)  # 取得した一覧を表示

        # receiptsが空でない場合
        if response_json['receipts']:
            receipt_id = response_json['receipts'][0]['id']
            receipt_id_list.append(receipt_id)
            partner_name = response_json['receipts'][0]['receipt_metadatum']['partner_name']
            issue_date = response_json['receipts'][0]['receipt_metadatum']['issue_date']
            amount = response_json['receipts'][0]['receipt_metadatum']['amount']
            # response_jsonをreceipt_{id}.jsonで保存
            with open(f"receipt_{receipt_id}_{issue_date}_{partner_name}_{amount}yen.json", "w", encoding="utf-8") as f:
                json.dump(response_json, f, ensure_ascii=False, indent=4)

        else:
            print(f"Upload number {upload_number} has no receipts.")

    else:
        print("Error:", response.json())

# 最後にreceipt_id_listをcsvで保存
with open(SAVE_PATH, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    for rid in receipt_id_list:
        writer.writerow([rid])

print("保存が完了しました。")
