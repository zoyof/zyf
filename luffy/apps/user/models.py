from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True)
    icon = models.ImageField(upload_to='icon', default='icon/default.jpg')

    class Meta:
        db_table = 'luffy_user'
        verbose_name = '用户名'
        verbose_name_plural = verbose_name
