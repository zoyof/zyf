from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('pay', views.PayViewSet, 'pay')
urlpatterns = [
    # path('', include(router.urls)),
    path('success/', views.AliPayView.as_view()),
]

urlpatterns += router.urls
