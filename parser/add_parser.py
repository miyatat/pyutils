# -*- coding: utf-8 -*-

from logging import getLogger
import argparse

logger = getLogger(__name__)


def get_parser(description):
    parser = argparse.ArgumentParser(description=description)
    return parser


def add_path_root_src(parser):
    """
    path_root_src is needed.
    Args:
        parser (argparse.ArgumentParser): parser instance from Argparse
    Returns:
        added parser instance
    """
    parser.add_argument(
        'path_root_src',
        action='store',
        nargs=None,
        const=None,
        default=None,
        type=str,
        choices=None,
        help='Directory path where your taken photo files are located.',
        metavar=None
    )
    return parser


def add_path_root_dst(parser):
    """
    path-root-dst is optional
    Args:
        parser (argparse.ArgumentParser): parser instance from Argparse
    Returns:
        added parser instance
    """
    parser.add_argument(
        '-d', '--path-root-dst',
        action='store',
        nargs='?',
        const=None,
        default=None,
        type=str,
        choices=None,
        help='Directory path where you want to create date folder and locate photo files.'
             ' (default: same as source directory)',
        metavar=None
    )
    return parser


def add_extensions(parser):
    """
    extensions is optional. 2 or more ok. Default 'jpg'
    Args:
        parser (argparse.ArgumentParser): parser instance from Argparse
    Returns:
        added parser instance
    """
    parser.add_argument(
        '-e', '--sort-files-extentions',
        action='store',
        nargs='+',
        const=None,
        default=['jpg'],
        type=str,
        choices=None,
        help='Extentions of file which you want to sort. (default: jpg)',
        metavar=None
    )
    return parser


def add_debug_mode(parser):
    """
    debug option.
    Args:
        parser:
    """
    parser.add_argument(
        '--debug',
        action='store_true',
        default=False,
        help='debug mode if this flag is set (default: False)'
    )


if __name__ == '__main__':
    pass
