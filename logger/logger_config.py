# -*- coding: utf-8 -*-

from logging import getLogger
from logging.config import dictConfig

import yaml

from dir_path import get_logger_yaml_path_name

logger = getLogger(__name__)


def set_logger(process_name):
    """
    所定のlogger設定ファイルを呼び出し、設定後のloggerを受け取る関数
    Args:
        process_name:
    """
    logger_config_yaml_path = get_logger_yaml_path_name(process_name)
    with open(logger_config_yaml_path, 'r') as f:
        logger_config = yaml.load(f)
    dictConfig(logger_config)
    logger.info('Success! logger loaded.')


if __name__ == '__main__':
    pass
