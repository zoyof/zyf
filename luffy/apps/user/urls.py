from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from user import views

router = SimpleRouter()
router.register('', views.MobileView, 'mobile')
router.register('register', views.RegisterView, 'register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view({'post': 'login'})),
    path('mobile_login/', views.LoginView.as_view({'post': 'mobile_login'})),
    path('sms/', views.LoginView.as_view({'get': 'send_sms'})),
]

urlpatterns += router.urls
