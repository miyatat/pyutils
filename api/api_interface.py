# -*- coding: utf-8 -*-

from logging import getLogger
import json
import hashlib

from bottle import response

logger = getLogger(__name__)


def check_salt_length(salt):
    """
    saltの長さをチェックする関数
    Args:
        salt (str): salt value used in API

    Returns:
        salt length is more than 5 or not. If not, raise error.
    """
    len_salt = len(salt)
    if len_salt < 5:
        logger.error('API config.salt value need more than 4')
        raise ValueError
    elif len_salt < 10:
        logger.warning('API config.salt value is less length.')
        return True
    else:
        return True


def check_token(token_str, token, salt):
    """
    tokenとtoken_strの文字列ペアが正しいかどうかを得る関数
    Args:
        token_str (str): token_str val in request
        token (str): token str val in request
        salt (str): salt value used in API

    Returns:
        digest == token
    """
    if token_str is None:
        logger.warning('token_str is None. Low security.')

    digest = hashlib.sha256((token_str + salt).encode('utf-8')).hexdigest()
    logger.info('input_digest= ' + digest)
    return digest == token


def return_internal_server_error(error_msg='Internal Server Error'):
    """
    インターナルサーバーエラーをレスポンスするインターフェース辞書を返す関数
    Args:
        error_msg (str): error message

    Returns:
        error response dict
    """
    response.status = 500
    response_dict = {
        "status": response.status,
        "error_msg": error_msg
    }
    logger.info(response_dict)
    return json.dumps(response_dict)


def return_not_found(error_msg='Not Found'):
    """
    URI not foundエラーをレスポンスするインターフェース辞書を返す関数
    Args:
        error_msg (str): error message

    Returns:
        error response dict
    """
    response.status = 404
    response_dict = {
        "status": response.status,
        "error_msg": error_msg
    }
    logger.info(response_dict)
    return json.dumps(response_dict)


def return_method_not_allowed(error_msg='Method Not Allowed'):
    """
    not allowed エラーをレスポンスするインターフェース辞書を返す関数
    Args:
        error_msg (str): error message

    Returns:
        error response dict
    """
    response.status = 405
    response_dict = {
        "status": response.status,
        "error_msg": error_msg
    }
    logger.info(response_dict)
    return json.dumps(response_dict)


def return_not_acceptable(error_msg='Not Acceptable'):
    """
    not acceptableエラーをレスポンスするインターフェース辞書を返す関数
    Args:
        error_msg (str): error message

    Returns:
        error response dict
    """
    response.status = 406
    response_dict = {
        "status": response.status,
        "error_msg": error_msg
    }
    logger.info(response_dict)
    return json.dumps(response_dict)


def return_bad_request(error_msg='Bad Request'):
    """
    bad requestエラーをレスポンスするインターフェース辞書を返す関数
    Args:
        error_msg (str): error message

    Returns:
        error response dict
    """
    response.status = 400
    response_dict = {
        "status": response.status,
        "error_msg": error_msg
    }
    logger.info(response_dict)
    return json.dumps(response_dict)


def return_unauthorized(error_msg='Unauthorized'):
    """
    unauthorized エラーをレスポンスするインターフェース辞書を返す関数
    Args:
        error_msg (str): error message

    Returns:
        error response dict
    """
    response.status = 401
    response_dict = {
        "status": response.status,
        "error_msg": error_msg
    }
    logger.info(response_dict)
    return json.dumps(response_dict)


def return_forbidden(error_msg='Forbidden'):
    """
    forbidden エラーをレスポンスするインターフェース辞書を返す関数
    Args:
        error_msg (str): error message

    Returns:
        error response dict
    """
    response.status = 403
    response_dict = {
        "status": response.status,
        "error_msg": error_msg
    }
    logger.info(response_dict)
    return json.dumps(response_dict)


def return_result(results_dict, msg='success'):
    """
    正しい処理が行われた際に、結果を返すインターフェース辞書を返す関数
    Args:
        results_dict(dict, str: object): result dict
        msg (str): message

    Returns:
        response dict
    """
    response.status = 200
    response_dict = {
        "status": response.status,
        "msg": msg
    }
    logger.info(response_dict)
    response_dict["results"] = results_dict
    return json.dumps(response_dict)


if __name__ == '__main__':
    pass
