from django.shortcuts import render

# Create your views here.
from rest_framework.serializers import Serializer
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet, ViewSetMixin
from rest_framework.generics import GenericAPIView, ListAPIView
from . import models
from . import serializer
from django.conf import settings


class BannerView(ViewSetMixin, ListAPIView):
    queryset = models.Banner.objects.all().filter(is_delete=False, is_show=True).order_by('orders')[:settings.BANNER_COUNT]
    serializer_class = serializer.BannerSerializer

def index(request):
    print(request.method)
    print('put执行了')
    return HttpResponse('ssss')