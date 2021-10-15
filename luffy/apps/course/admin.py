
from django.contrib import admin


from . import models

admin.site.register(models.Course)
admin.site.register(models.CourseSection)
admin.site.register(models.CourseChapter)
admin.site.register(models.CourseCategory)
admin.site.register(models.Teacher)