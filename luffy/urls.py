from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings


from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),

    path('api/v1/home/', include('home.urls')),
    path('api/v1/user/', include('user.urls')),
    path('api/v1/course/', include('course.urls')),
    path('api/v1/order/', include('order.urls')),
    # re_path('media/(?P<path>.*?)', serve, {'document_root': settings.MEDIA_ROOT}),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
