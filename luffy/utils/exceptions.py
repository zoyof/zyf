from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.views import Response
from rest_framework import status

from util import log

logger = log.get_logger()


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:  # drf没有处理的，django的异常
        # response = Response({'detail': '服务器异常，请重试...'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = Response({'code': 999, 'msg': '服务器异常，请重试...'})
        print(response)
    else:
        try:
            msg = response.data['detail']
        except Exception:
            msg = '未知异常'
        response = Response({'code': 998, 'msg': msg})
    # 记录服务器异常,drf和django的异常，都记录
    # 时间，哪个ip地址，用户id，哪个视图类，出了什么错
    logger.critical('%s' % exc)
    return response
