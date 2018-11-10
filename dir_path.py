# -*- coding: utf-8 -*-

from logging import getLogger
import os

import repo

logger = getLogger(__name__)

SRC_DIR_NAME = repo.__path__[0]


def join_and_makedirs(*keys):
    path_name = ''
    for key in keys:
        path_name = os.path.join(path_name, key)
    os.makedirs(path_name, exist_ok=True)
    print('define ' + path_name)
    return path_name


STORAGE_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'storage')
TASKS_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'tasks')
TESTS_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'tests')
CONFIG_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'config')
MODEL_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'model')
SANDBOX_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'sandbox')
CONTROLLERS_DIR_NAME = join_and_makedirs(SRC_DIR_NAME, 'controllers')


if __name__ == '__main__':
    pass
