# -*- coding: utf-8 -*-
import glob
import os
from logging import getLogger

logger = getLogger(__name__)


def get_latest_modified_file_path(dir_name, extension='*'):
    """
    dir内のファイルで最も最近、変更を加えられたファイルの絶対パスを返す関数
    Args:
        dir_name (str): directory name
        extension (str, optional): Use it if you filter by extension

    Returns:
        Latest modified file path name str in dir.
    """
    target = os.path.join(dir_name, extension)
    files = [(f, os.path.getmtime(f)) for f in glob.glob(target)]

    if len(files) >= 1:
        latest_modified_file_path = sorted(files, key=lambda files: files[1])[-1][0]
        return latest_modified_file_path
    else:
        logger.warning('No file in' + dir_name)
        return None


def delete_except_latest_files(dir_name, left_num=20, delete_flag=True):
    """
    直近に変更が加えられた・作成されたファイルのうちし定数を残して残りを削除する関数
    Args:
        dir_name (str): directory name
        left_num (int, optional): The number of files you want to leave
        delete_flag (bool, optional): If true, the exceptional files will be deleted
    """
    target = os.path.join(dir_name, '*')
    files_tuple = [(f, os.path.getmtime(f)) for f in glob.glob(target)]
    if len(files_tuple) >= 1:
        latest_file_path_list = sorted(files_tuple, key=lambda files: files[1], reverse=True)
        if len(latest_file_path_list) > left_num:
            latest_left_num = [x[0] for x in latest_file_path_list[:left_num]]
            except_latest_left_num = [x[0] for x in latest_file_path_list[left_num:]]
            latest_filename_list = [os.path.basename(x) for x in latest_left_num]

            logger.info('latest ' + str(left_num) + '=')
            [logger.info(x) for x in latest_filename_list]
            if delete_flag:
                [os.remove(filepath) for filepath in except_latest_left_num]
                logger.info('Deleted except latest ' + str(left_num) + '.')
        else:
            latest_left_num = [x[0] for x in latest_file_path_list]
            latest_filename_list = [os.path.basename(x) for x in latest_left_num]

            logger.info('Less than / Equal to ' + str(left_num) + ' files in ' + dir_name + '\n' + 'latest list=')
            [logger.info(x) for x in latest_filename_list]

    else:
        logger.warning('No file in' + dir_name)


def get_all_file_path_in_dir(dir_name):
    """
    dir内の全てのファイルのパスを取得する関数
    Args:
        dir_name (str): directory name

    Returns:
        All file path name str list
    """
    all_file_path_list = [r for r in glob.glob(dir_name + '/*')]
    return all_file_path_list


if __name__ == '__main__':
    pass
