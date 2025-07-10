import requests
import csv
import time
import json

# Freee APIの設定
API_BASE_URL = "https://api.freee.co.jp/api/1/deals/"

# 事業所
ACCESS_TOKEN = ""
COMPANY_ID = ""
# CSVファイルのパス
CSV_FILE_PATH = "deals.csv"

# ヘッダー
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Api-Version": "2020-06-15",
    "Content-Type": "application/json"
}


def fetch_deal(deal_id):
    """取引IDを指定してAPIからデータを取得"""
    url = f"{API_BASE_URL}{deal_id}?company_id={COMPANY_ID}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching deal {deal_id}: {response.status_code}, {response.text}")
        return None


def update_deal(deal):
    """取得した取引情報を基に更新用データを作成し、PUTリクエストを送信"""
    deal_id = deal['deal']['id']

    # 必須フィールドを保持
    update_payload = {
        "issue_date": deal['deal']['issue_date'],
        "type": deal['deal']['type'],
        "company_id": COMPANY_ID,
        "details": []
    }

    # partner_id, partner_code, ref_number を None の場合は除外
    if deal['deal'].get('partner_id') is not None:
        update_payload["partner_id"] = deal['deal']['partner_id']
    if deal['deal'].get('partner_code') is not None:
        update_payload["partner_code"] = deal['deal']['partner_code']
    if deal['deal'].get('ref_number') is not None:
        update_payload["ref_number"] = deal['deal']['ref_number']

    # detailsの更新
    for detail in deal['deal']['details']:
        updated_detail = {
            "id": detail['id'],
            "tax_code": detail['tax_code'],
            "account_item_id": detail['account_item_id'],
            "amount": detail['amount'],
            "section_id": 3305964  # Makesteinで追加するセクションID
            # "section_id": 3305963  # E-INSで追加するセクションID
        }

        # item_id, tag_ids, description を None の場合は除外
        if detail.get('item_id') is not None:
            updated_detail["item_id"] = detail['item_id']
        if detail.get('tag_ids') is not None:
            original_tag_ids = detail['tag_ids']
            # original_tag_ids.append(28624048)
            updated_detail["tag_ids"] = original_tag_ids
        # else:
        #     updated_detail["tag_ids"] = [28624048]
        if detail.get('description') is not None:
            updated_detail["description"] = detail['description']

        update_payload["details"].append(updated_detail)

    # PUTリクエストを送信
    url = f"{API_BASE_URL}{deal_id}"
    response = requests.put(url, headers=HEADERS, data=json.dumps(update_payload))

    if response.status_code == 200:
        print(f"Successfully updated deal ID: {deal_id}")
    else:
        print(f"Error updating deal {deal_id}: {response.status_code}, {response.text}")


def read_csv(file_path):
    """CSVから取引IDのリストを読み取る"""
    deal_ids = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # 空行を無視
                deal_ids.append(row[0])  # 取引IDは1列目にあると仮定
    return deal_ids


def main():
    deal_ids = read_csv(CSV_FILE_PATH)

    for deal_id in deal_ids:
        print(f"Fetching deal ID: {deal_id}")
        deal_data = fetch_deal(deal_id)

        if deal_data:
            update_deal(deal_data)

        time.sleep(1)  # API制限回避


if __name__ == "__main__":
    main()
