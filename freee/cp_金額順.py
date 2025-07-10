import os
import shutil
import re

def copy_receipts_with_amount_id(src_folder, dst_folder):
    """
    receiptsフォルダ内の画像を金額順フォルダにコピーする。
    コピー先ファイル名は10桁の数字ID（amount）+ 元ファイル名。

    :param src_folder: 元フォルダパス
    :param dst_folder: コピー先フォルダパス
    """
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for filename in os.listdir(src_folder):
        if filename.endswith(".jpg"):
            # 正規表現で金額を取得
            match = re.search(r"_(\d+)yen\.jpg$", filename)
            if match:
                amount_str = match.group(1)
                try:
                    amount = int(amount_str)
                    # 10桁数字IDにフォーマット
                    amount_id = f"{amount:010d}"
                except ValueError:
                    print(f"金額が数値変換できません: {filename}")
                    continue
            else:
                print(f"金額が見つかりません: {filename}")
                continue

            # コピー元とコピー先パス作成
            src_path = os.path.join(src_folder, filename)
            dst_filename = f"{amount_id}_{filename}"
            dst_path = os.path.join(dst_folder, dst_filename)

            shutil.copy2(src_path, dst_path)
            print(f"Copied: {dst_filename}")

# 実行例
copy_receipts_with_amount_id("receipts_B級", "金額順")
