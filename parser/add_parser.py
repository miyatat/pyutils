# -*- coding: utf-8 -*-

from logging import getLogger

logger = getLogger(__name__)


def add_data_name(parser):
    """
    data_nameを引数として取るためのparserを追加するための関数
    Args:
        parser (argparse.ArgumentParser): parser instance from Argparse

    Returns:
        added parser instance
    """
    parser.add_argument(
        'data_name',
        action='store',
        nargs=None,
        const=None,
        default=None,
        type=str,
        choices=None,
        help='data_name detector.',
        metavar=None
    )
    return parser


def add_img_api_type(parser):
    """
    img_api_typeを引数として取るためのparserを追加するための関数
    Args:
        parser (argparse.ArgumentParser): parser instance from Argparse

    Returns:
        added parser instance
    """
    parser.add_argument(
        'img_api_type',
        action='store',
        nargs=None,
        const=None,
        default='google',
        type=str,
        choices=None,
        help='"google" or "bing". Image API type what you want to use.',
        metavar=None
    )
    return parser


if __name__ == '__main__':
    pass
