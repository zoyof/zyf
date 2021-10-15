from django.db import models
from utils.models import BaseModel


# Create your models here.

class Banner(BaseModel):
    title = models.CharField(max_length=16, unique=True, verbose_name='名称')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    link = models.CharField(max_length=64, verbose_name='跳转链接')
    info = models.TextField(verbose_name='详情')  # 也可以用详情表，宽高出处

    class Meta:
        db_table = 'luffy_banner'
        verbose_name_plural = '轮播图表'

    def __str__(self):
        return self.title
