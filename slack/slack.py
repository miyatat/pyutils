# -*- coding: utf-8 -*-

from logging import getLogger

import yaml
import slackweb

from dir_path import SLACK_CONFIG_PATH_NAME

logger = getLogger(__name__)


def read_config():
    with open(SLACK_CONFIG_PATH_NAME, 'r')as f:
        config_dict = yaml.safe_load(f)
        logger.info('slack config loaded.')

    return config_dict


def send_slack(msg):
    config = read_config()
    slack = slackweb.Slack(url=config['webhool'])
    slack.notify(text=msg)
    logger.info('slack sent.')


if __name__ == '__main__':
    pass
