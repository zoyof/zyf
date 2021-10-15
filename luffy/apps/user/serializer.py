from rest_framework import serializers
from . import models
import re
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from django.core.cache import cache
from django.conf import settings


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=16, min_length=2)

    class Meta:
        model = models.User
        fields = ['username', 'password']

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(user)
        self.context['token'] = token
        self.context['username'] = user.username
        return attrs

    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        if re.match(r'^1[3-9][0-9]{9}$', username):
            user = models.User.objects.filter(mobile=username).first()
        elif re.match(r'^.+@.+$', username):
            user = models.User.objects.filter(email=username).first()
        else:
            user = models.User.objects.filter(username=username).first()

        if user and user.check_password(password):
            return user
        else:
            raise ValidationError('用户名或密码错误')

    def _get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class MobileLoginSerializer(serializers.ModelSerializer):
    # 重写它的原因，unique=True
    mobile = serializers.CharField()
    # code 由于不是表的字段，所有必须重写
    code = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['code', 'mobile']

    # 用户校验和签发token
    def validate(self, attrs):
        '''
        1 校验code是否正确：从缓存中根据手机号获取code，比较

        2 根据手机号，拿到当前用户，
        3 根据用户，签发token
        3 把token放到序列化类的对象中
        '''

        user = self._get_user(attrs)
        token = self._get_token(user)
        # 上下文，是个字典
        self.context['token'] = token
        self.context['username'] = user.username

        return attrs

    def _get_user(self, attrs):  # 不是私有，但尽量只给内部用
        code = attrs.get('code')
        mobile = attrs.get('mobile')
        # 校验code
        cache_code = cache.get(settings.CACHE_SMS % mobile)
        if cache_code and code == cache_code:
            user = models.User.objects.filter(mobile=mobile).first()
            if user:
                return user
            else:
                raise ValidationError('用户名或密码错误')
        else:
            raise ValidationError('验证码错误')

    def _get_token(self, user):
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


class RegisterUserSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4)

    class Meta:
        model = models.User
        fields = ['mobile', 'password', 'code']
        extra_kwargs = {'mobile': {'write_only': True},
                        'password': {'write_only': True}, 'username': {'read_only': True}}

    def validate(self, attrs):
        code = attrs.get('code')
        mobile = attrs.get('mobile')
        # 校验code
        cache_code = cache.get(settings.CACHE_SMS % mobile)
        if cache_code and code == cache_code:
            attrs.pop('code')
            attrs['username'] = mobile
        else:
            raise ValidationError({'detail': '验证码错误'})
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user
