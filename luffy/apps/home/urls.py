from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('banner', views.BannerView, 'banner')
urlpatterns = [
    # path('', include(router.urls)),
]

urlpatterns += router.urls
