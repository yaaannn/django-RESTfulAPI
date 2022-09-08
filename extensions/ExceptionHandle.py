import logging
import json
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def handle_re_str(datas: dict):
    '''处理默认的异常信息，将字典数据转为字符串数据'''
    finally_str = ''
    for key in datas:
        res = '%s: ' % key
        if isinstance(datas[key], str):
            finally_str += (res + datas[key])
        elif isinstance(datas[key], list):
            for item in datas[key]:
                if isinstance(item, str):
                    res += item
                elif isinstance(item, dict):
                    res += handle_re_str(item)
            finally_str += res
        else:
            finally_str += res
        finally_str += '; '
    return finally_str


def base_exception_handler(exc, context):
    '''
    用于处理drf的异常定制返回，目的是统一返回信息，只有drf出现异常时才会执行，其他情况不执行
    '''
    logging.debug('DRF主动提示异常')
    response = exception_handler(exc, context)
    if response:
        logging.debug('可处理异常')
        logging.debug(response.data)
        msg = ''
        new_data = json.loads(json.dumps(response.data))
        msg = handle_re_str(new_data)[:-2]
        code = 0 if response.status_code == 200 else 2
        return Response({"message": msg, "errorCode": code, "data": {}}, status=status.HTTP_200_OK)
    logging.debug('未知异常')
    logging.exception(exc)
    return Response({"message": str(exc), "errorCode": 1, "data": {}}, status=status.HTTP_200_OK)