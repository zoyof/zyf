from rest_framework import serializers

from .models import CourseCategory, Course, Teacher, CourseChapter, CourseSection


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'title', 'signature', 'image', 'brief', 'role_name']


class CourseSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()

    class Meta:
        model = Course
        fields = ['id', 'name', 'students', 'teacher', 'sections', 'pub_sections', 'price', 'course_section_list',
                  'course_img', 'level_name']


class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = ['id', 'name', 'get_section_type_display', 'section_link', 'duration', 'free_trail']


class CourseChapterSerializer(serializers.ModelSerializer):
    coursesections = CourseSectionSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'name', 'summary', 'pub_date', 'coursesections']
