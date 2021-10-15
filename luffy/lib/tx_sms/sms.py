import random
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
from .settings import *
from utils.log import get_logger

logger = get_logger()


def get_code():
    code_str = ''
    for i in range(4):
        numbers = str(random.randint(0, 9))
        code_str += numbers
    return code_str


def send_sms(phone, code):
    ssender = SmsSingleSender(APPID, APPKEY)
    params = [code]  # 当模板没有参数时，`params = []`
    try:
        result = ssender.send_with_param(86, phone,
                                         TEMPLATE_ID, params, sign=SMS_SIGN, extend="", ext="")

    except Exception as e:
        logger.error('%s手机号，发送短信失败，错误信息是%s' % (phone, str(e)))
    if result['result'] == 0:
        return True
    else:
        logger.warning('%s手机号发送短信失败,失败原因是%s' % (phone, result['errmsg']))
        return False


if __name__ == '__main':
    print(get_code())
