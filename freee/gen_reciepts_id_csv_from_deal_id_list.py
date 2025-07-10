import requests
import csv
import time
import os

# Freee APIの設定
API_BASE_URL = "https://api.freee.co.jp/api/1/deals/"

# 事業所
ACCESS_TOKEN = ""
COMPANY_ID = ""


# 入出力ファイルのパス
INPUT_CSV_FILE = "deals.csv"  # 取引IDを含むCSV,ブラウザからダウンロードして加工し作成
OUTPUT_CSV_FILE = "receipts_e-ins.csv"  # 出力するレシートIDのCSV

# ヘッダー
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Api-Version": "2020-06-15"
}


def fetch_deal(deal_id):
    """取引IDを指定してAPIから取引データを取得し、レシートIDと取引日を取得"""
    url = f"{API_BASE_URL}{deal_id}?company_id={COMPANY_ID}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching deal {deal_id}: {response.status_code}, {response.text}")
        return None


def read_csv(file_path):
    """CSVから取引IDのリストを読み取る"""
    deal_ids = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # 空行を無視
                deal_ids.append(row[0])  # 取引IDは1列目にあると仮定
    return deal_ids


def save_receipts_to_csv(receipts_data):
    """取得したレシートIDをCSVに保存"""
    with open(OUTPUT_CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["issue_date", "deal_id", "receipt_id"])  # ヘッダー行を追加
        writer.writerows(receipts_data)  # データを書き込み


def main():
    deal_ids = read_csv(INPUT_CSV_FILE)
    receipts_data = []

    for deal_id in deal_ids:
        print(f"Fetching deal ID: {deal_id}")
        deal_data = fetch_deal(deal_id)

        if deal_data and 'deal' in deal_data:
            issue_date = deal_data['deal'].get('issue_date', 'unknown')  # 取引日
            if 'receipts' in deal_data['deal']:
                for receipt in deal_data['deal']['receipts']:
                    receipt_id = receipt['id']
                    receipts_data.append([issue_date, deal_id, receipt_id])
                    print(f"Added receipt ID: {receipt_id} (Deal ID: {deal_id}, Date: {issue_date})")

        time.sleep(1)  # API制限回避

    # CSVに保存
    save_receipts_to_csv(receipts_data)
    print(f"Receipts data saved to {OUTPUT_CSV_FILE}")


if __name__ == "__main__":
    main()
