from rest_framework.viewsets import ViewSet
from . import serializer
from utils.response import APIResponse
from rest_framework.decorators import action
from . import models
from rest_framework.exceptions import APIException
from lib import tx_sms
import re
from django.core.cache import cache
from django.conf import settings
from .util import SMSThrottle


# Create your views here.

class LoginView(ViewSet):
    def login(self, request):
        ser = serializer.LoginSerializer(data=request.data)
        if ser.is_valid():
            token = ser.context.get('token')
            username = ser.context.get('username')
            return APIResponse(msg='登陆成功', username=username, token=token)

        else:
            return APIResponse(code=101, msg='用户名或密码错误')

    def send_sms(self, request):
        mobile = request.query_params.get('mobile')
        if mobile and re.match('^1[3-9][0-9]{9}$', mobile):
            code = tx_sms.get_code()
            cache.set(settings.CACHE_SMS % mobile, code)
            res = tx_sms.send_sms(mobile, code)
            if res:
                return APIResponse(msg='短信发送成功')
            else:
                raise APIException('短信发送失败')
        else:
            raise APIException('手机号不合法')

    def mobile_login(self, request):
        ser = serializer.MobileLoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        if ser.is_valid():
            token = ser.context.get('token')
            username = ser.context.get('username')
            return APIResponse(msg='登陆成功', username=username, token=token)


class MobileView(ViewSet):
    @action(methods=['GET'], detail=False)
    def mobile(self, request):
        mobile = request.query_params.get('mobile')
        try:
            models.User.objects.get(mobile=mobile)
        except Exception:
            raise APIException('手机号不存在')
        return APIResponse(is_exisit=True)

    @action(methods=['GET'], detail=False, url_path='sms', throttle_classes=[SMSThrottle])
    def send_sms(self, request):
        mobile = request.query_params.get('mobile')
        if mobile and re.match('^1[3-9][0-9]{9}$', mobile):
            code = tx_sms.get_code()
            cache.set(settings.CACHE_SMS % mobile, code)
            res = tx_sms.send_sms(mobile, code)
            if res:
                return APIResponse(msg='短信发送成功')
            else:
                raise APIException('短信发送失败')
        else:
            raise APIException('手机号不合法')


from rest_framework.viewsets import ViewSetMixin, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from .models import User


class RegisterView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializer.RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        super().create(self, request, *args, **kwargs)
        return APIResponse(msg='注册成功')
