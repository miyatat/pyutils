import requests
import csv
import time

# Freee APIの設定
API_BASE_URL = "https://api.freee.co.jp/api/1/receipts/"

# 事業所：
ACCESS_TOKEN = ""
COMPANY_ID = ""

# CSVファイルのパス
CSV_FILE_PATH = "receipts/receipts.csv"  # receipt_id を含むCSV,自分で作成
LOG_FILE = "delete_receipts_log.csv"

# ヘッダー
HEADERS = {
    "accept": "*/*",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Api-Version": "2020-06-15"
}


def delete_receipt(receipt_id):
    """指定されたレシートIDのレシートを削除"""
    url = f"{API_BASE_URL}{receipt_id}?company_id={COMPANY_ID}"
    response = requests.delete(url, headers=HEADERS)

    if response.status_code == 204:
        print(f"✅ Successfully deleted receipt ID: {receipt_id}")
        return True
    else:
        print(f"❌ Error deleting receipt ID {receipt_id}: {response.status_code}, {response.text}")
        return False


def read_receipt_ids(file_path):
    """CSVからレシートIDのリストを読み取る"""
    receipt_ids = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # ヘッダー行をスキップ
        for row in reader:
            if row and len(row) >= 3:  # issue_date, deal_id, receipt_id の3列がある前提
                receipt_ids.append(row[2])  # 3列目が receipt_id
    return receipt_ids


def log_error(receipt_id, error_message):
    """削除に失敗したレシートIDをCSVに記録"""
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([receipt_id, error_message])


def main():
    receipt_ids = read_receipt_ids(CSV_FILE_PATH)

    # ログファイルのヘッダーを初期化
    with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["receipt_id", "error_message"])

    # 各レシートを削除
    for receipt_id in receipt_ids:
        print(f"🗑️ Deleting receipt ID: {receipt_id}")
        success = delete_receipt(receipt_id)

        if not success:
            log_error(receipt_id, "Failed to delete receipt")

        time.sleep(1)  # API制限回避

    print(f"🎯 Process completed. Check {LOG_FILE} for errors if any.")


if __name__ == "__main__":
    main()
