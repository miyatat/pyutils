# -*- coding: utf-8 -*-

from logging import getLogger

from bottle import route, error, hook, request, default_app, run

from . import api_interface

logger = getLogger(__name__)

# bottleのroutingを管理するモジュール
# https://bottlepy.org/docs/dev/等の記事を参考


@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')


@error(500)
def error500(error):
    return api_interface.return_internal_server_error()


@error(404)
def error404(error):
    return api_interface.return_not_found('URI not found')


@route('/api_name', method='GET')
def function_name():
    return api_interface.return_result({}, 'API has launched.')


if __name__ == '__main__':
    pass
