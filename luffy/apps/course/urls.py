from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from course import views

router = SimpleRouter()
router.register('category', views.CourseCategoryViewSet, 'category')
router.register('actual', views.CourseViewSet, 'actual')
router.register('chapter', views.CourseChapterViewSet, 'chapter')
router.register('search', views.CourseSearchViewSet, 'search')
urlpatterns = [

]

urlpatterns += router.urls
