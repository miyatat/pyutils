import requests
import csv
import time

# Freee APIの設定
API_BASE_URL = "https://api.freee.co.jp/api/1/deals/"
# 事業所：
ACCESS_TOKEN = ""
COMPANY_ID = ""


# CSVファイルのパス
CSV_FILE_PATH = "deals.csv" # 取引IDを含むCSV,ブラウザからダウンロードして加工し作成
LOG_FILE = "delete_log.csv"

# ヘッダー
HEADERS = {
    "accept": "*/*",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Api-Version": "2020-06-15"
}


def delete_deal(deal_id):
    """指定された取引IDの取引を削除"""
    url = f"{API_BASE_URL}{deal_id}?company_id={COMPANY_ID}"
    response = requests.delete(url, headers=HEADERS)

    if response.status_code == 204:
        print(f"Successfully deleted deal ID: {deal_id}")
        return True
    else:
        print(f"Error deleting deal ID {deal_id}: {response.status_code}, {response.text}")
        return False


def read_csv(file_path):
    """CSVから取引IDのリストを読み取る"""
    deal_ids = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # 空行を無視
                deal_ids.append(row[0])  # 取引IDは1列目にあると仮定
    return deal_ids


def log_error(deal_id, error_message):
    """削除に失敗した取引IDをCSVに記録"""
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([deal_id, error_message])


def main():
    deal_ids = read_csv(CSV_FILE_PATH)

    # ログファイルのヘッダーを初期化
    with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["deal_id", "error_message"])

    # 各取引を削除
    for deal_id in deal_ids:
        print(f"Deleting deal ID: {deal_id}")
        success = delete_deal(deal_id)

        if not success:
            log_error(deal_id, "Failed to delete deal")

        time.sleep(1)  # API制限回避

    print(f"Process completed. Check {LOG_FILE} for errors if any.")


if __name__ == "__main__":
    main()
