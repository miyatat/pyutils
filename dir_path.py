# -*- coding: utf-8 -*-

from logging import getLogger
import os

logger = getLogger(__name__)

SRC_DIR_NAME = os.path.dirname(os.path.abspath(__file__))


def join_and_makedirs(*keys):
    path_name = ''
    for key in keys:
        path_name = os.path.join(path_name, key)
    os.makedirs(path_name, exist_ok=True)
    return path_name


STORAGE_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'storage')



if __name__ == '__main__':
    pass
