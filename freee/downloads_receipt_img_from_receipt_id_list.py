import requests
import csv
import time
import os
import glob


# Freee APIの設定
API_BASE_URL = "https://api.freee.co.jp/api/1/receipts/"
# 事業所：
ACCESS_TOKEN = ""
COMPANY_ID = ""

# CSVファイルのパス
CSV_FILE_PATH = "receipts/receipts.csv"  # receipt_id を含むCSV,自分で作成
DOWNLOAD_FOLDER = "receipts"  # ダウンロードしたファイルを保存するフォルダ

# ヘッダー
HEADERS = {
    "accept": "text/csv",
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "X-Api-Version": "2020-06-15"
}


def find_json_files_with_prefix(prefix, folder='.'):
    """
    指定フォルダから {prefix}_*.json 形式のファイル名を取得する

    :param prefix: ファイル名の先頭の特定文字列
    :param folder: 検索するフォルダ（デフォルトはカレントディレクトリ）
    :return: 該当ファイルのファイル名リスト
    """
    pattern = os.path.join(folder, f"{prefix}_*.json")
    files = glob.glob(pattern)
    # ファイル名だけにする場合
    filenames = [os.path.basename(f) for f in files]
    assert len(filenames) == 1
    return filenames[0]

def download_receipt(receipt_id):
    filenames = find_json_files_with_prefix(f'receipt_{receipt_id}')
    """レシートIDを指定してダウンロード"""
    url = f"{API_BASE_URL}{receipt_id}/download?company_id={COMPANY_ID}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        # ファイル名のフォーマット
        file_path = os.path.join(DOWNLOAD_FOLDER, filenames.replace('.json','.jpg'))
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded receipt ID: {receipt_id}  -> {file_path}")
    else:
        print(f"Error downloading receipt {receipt_id} : {response.status_code}, {response.text}")


def read_csv(file_path):
    """CSVからReceipt IDのリストを読み取る"""
    receipt_ids = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # 空行を無視
                receipt_ids.append(row[0])  # 取引IDは1列目にあると仮定
    return receipt_ids


def main():
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    receipt_ids = read_csv(CSV_FILE_PATH)
    for receipt_id in receipt_ids:
        download_receipt(receipt_id)
        time.sleep(1)  # API制限回避

if __name__ == "__main__":
    main()
