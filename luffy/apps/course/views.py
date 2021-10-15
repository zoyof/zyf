from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from .models import CourseCategory, Course, CourseChapter
from .serializer import CourseCategorySerializer, CourseSerializer, CourseChapterSerializer
from .page import CommonPageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class CourseCategoryViewSet(GenericViewSet, ListModelMixin):
    queryset = CourseCategory.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseCategorySerializer


class CourseViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Course.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseSerializer
    pagination_class = CommonPageNumberPagination
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['id', 'students', 'price']
    filter_fields = ['course_category']


class CourseChapterViewSet(GenericViewSet, ListModelMixin):
    queryset = CourseChapter.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseChapterSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']


class CourseSearchViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Course.objects.all().filter(is_delete=False, is_show=True).order_by('orders')
    serializer_class = CourseSerializer
    pagination_class = CommonPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'brief']

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
