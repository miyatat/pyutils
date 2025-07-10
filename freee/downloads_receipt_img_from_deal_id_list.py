import requests
import csv
import time
import os

# Freee APIの設定
API_BASE_URL = "https://api.freee.co.jp/api/1/receipts/"
# 事業所：
ACCESS_TOKEN = ""
COMPANY_ID = ""

# CSVファイルのパス
CSV_FILE_PATH = "deals.csv" # 取引IDを含むCSV,ブラウザからダウンロードして加工し作成
DOWNLOAD_FOLDER = "receipts"  # ダウンロードしたファイルを保存するフォルダ

# ヘッダー
HEADERS = {
    "accept": "text/csv",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Api-Version": "2020-06-15"
}


def fetch_deal(deal_id):
    """取引IDを指定してAPIから取引データを取得し、レシートIDと取引日を取得"""
    url = f"https://api.freee.co.jp/api/1/deals/{deal_id}?company_id={COMPANY_ID}"
    response = requests.get(url, headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "accept": "application/json",
        "X-Api-Version": "2020-06-15"
    })

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching deal {deal_id}: {response.status_code}, {response.text}")
        return None


def download_receipt(receipt_id, deal_id, issue_date):
    """レシートIDを指定してダウンロード"""
    url = f"{API_BASE_URL}{receipt_id}/download?company_id={COMPANY_ID}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        # ファイル名のフォーマット
        file_path = os.path.join(DOWNLOAD_FOLDER, f"date_{issue_date}_deal_id_{deal_id}_receipt_{receipt_id}.jpg")
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded receipt ID: {receipt_id} (Deal ID: {deal_id}, Date: {issue_date}) -> {file_path}")
    else:
        print(f"Error downloading receipt {receipt_id} (Deal ID: {deal_id}, Date: {issue_date}): {response.status_code}, {response.text}")


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
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    deal_ids = read_csv(CSV_FILE_PATH)

    for deal_id in deal_ids:
        print(f"Fetching deal ID: {deal_id}")
        deal_data = fetch_deal(deal_id)

        if deal_data and 'deal' in deal_data:
            issue_date = deal_data['deal'].get('issue_date', 'unknown')  # 取引日がなければ 'unknown'
            if 'receipts' in deal_data['deal']:
                for receipt in deal_data['deal']['receipts']:
                    receipt_id = receipt['id']
                    download_receipt(receipt_id, deal_id, issue_date)
                    time.sleep(1)  # API制限回避


if __name__ == "__main__":
    main()
