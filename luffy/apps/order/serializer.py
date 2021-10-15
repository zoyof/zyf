from . import models
from course.models import Course
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from lib.alipay import alipay, gateway
import uuid
from django.conf import settings


class PaySerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)

    class Meta:
        model = models.Order
        fields = ['subject', 'total_amount', 'pay_type', 'courses']
        extra_kwargs = {
            'subject': {'required': True},
            'total_amount': {'required': True}
        }

    def _check_total_amount(self, attrs):
        total_amount = attrs.get('total_amount')
        real_amount = 0
        for course in attrs.get('courses'):
            real_amount += course.price
        if not total_amount == real_amount:
            raise ValidationError({'detail': '价格不合法'})

    def _get_user(self):
        return self.context['request'].user

    def _get_out_trade_no(self):

        return str(uuid.uuid4()).replace('-', '')

    def _get_pay_url(self, attrs, out_trade_no):

        res = alipay.api_alipay_trade_page_pay(
            subject=attrs.get('subject'),
            total_amount=float(attrs.get('total_amount')),
            out_trade_no=out_trade_no,
            return_url=settings.RETURN_URL,
            notify_url=settings.NOTIFY_URL,
        )


        return gateway + res

    def _before_create(self, attrs, user, out_trade_no, pay_url):

        attrs['user'] = user
        attrs['out_trade_no'] = out_trade_no
        self.context['pay_url'] = pay_url

    def validate(self, attrs):
        self._check_total_amount(attrs)
        user = self._get_user()
        out_trade_no = self._get_out_trade_no()
        pay_url = self._get_pay_url(attrs, out_trade_no)
        self._before_create(attrs, user, out_trade_no, pay_url)

        return attrs

    def create(self, validated_data):
        courses = validated_data.pop('courses')
        order = models.Order.objects.create(**validated_data)
        for course in courses:
            models.OrderDetail.objects.create(order=order, course=course, price=course.price, real_price=course.price)

        return order
