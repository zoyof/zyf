from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from .models import Order
from utils.response import APIResponse
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
# 登录才能使用，认证类:自己写一个认证类  使用jwt内置的认证类，配合一个权限类
from .serializer import PaySerializer


class PayViewSet(GenericViewSet, CreateModelMixin):
    authentication_classes = [JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = PaySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)  # 字段自己的校验，局部钩子，全局钩子
        self.perform_create(serializer)
        pay_url = serializer.context['pay_url']
        return APIResponse(pay_url=pay_url)


from . import models
from utils.log import get_logger
from rest_framework.response import Response

logger = get_logger()


class AliPayView(APIView):
    def post(self, request):
        # 支付宝post回调，内网测不了
        try:
            result_data = request.data.dict()
            # 订单号，我们给的
            out_trade_no = result_data.get('out_trade_no')
            # 签名
            signature = result_data.pop('sign')
            from lib.alipay import alipay
            # sdk的验证签名方法
            result = alipay.verify(result_data, signature)
            if result and result_data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
                models.Order.objects.filter(out_trade_no=out_trade_no).update(order_status=1)
                logger.warning('%s订单支付成功' % out_trade_no)
                return Response('success')
            else:
                logger.error('%s订单支付失败' % out_trade_no)
        except:
            pass
        return Response('failed')

    def get(self, request):
        # 咱们前端，验证用
        print('来了')
        out_trade_no = request.query_params.get('out_trade_no')
        try:
            models.Order.objects.get(out_trade_no=out_trade_no, order_status=1)
            return APIResponse(result=True)
        except:
            return APIResponse(code=101, msg='error', result=False)
