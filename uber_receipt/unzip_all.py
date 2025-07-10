from logging import getLogger
import zipfile
import os

from utils.general_utils import get_glob_list

logger = getLogger(__name__)
def unzip_and_copy(zip_file_path, target_directory):
    # ZIPファイルを開く
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # ZIPファイルの中身を指定されたディレクトリに展開
        zip_ref.extractall(target_directory)
    print(f"ZIPファイル {zip_file_path} の内容が {target_directory} にコピーされました。")

if __name__ == '__main__':
    target_directory = '/home/einstein/Downloads/uber_reciepts'  # コピー先のディレクトリ

    zip_list = get_glob_list('/home/einstein/Downloads/uber_reciepts/', 'zip')
    for zip_file in zip_list:
        # 使用例
        unzip_and_copy(zip_file, target_directory)
