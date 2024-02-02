from logging import getLogger
from logging.config import dictConfig

import yaml

from config.load_config import setting_dict
logger = getLogger(__name__)


logger_yaml_path = setting_dict['logger']['yaml_path']

def set_logger(process_name):
    """
    所定のlogger設定ファイルを呼び出し、設定後のloggerを受け取る関数
    Args:
        process_name:
    """
    logger_config_yaml_path = logger_yaml_path
    with open(logger_config_yaml_path, 'r', encoding='utf-8') as file:
        # YAMLファイルを読み込んでPythonの辞書に変換
        logger_config = yaml.safe_load(file)
    dictConfig(logger_config)
    logger.info('Success! logger loaded.')
    logger.info(f'process_name:{process_name}, logging start.')


if __name__ == '__main__':
    set_logger('set logger test')
