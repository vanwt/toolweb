from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    id = models.UUIDField(verbose_name="ID", primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField('手机号', max_length=11, null=False)
    realname = models.CharField('真实姓名', max_length=4, null=False)
    is_active = models.BooleanField(verbose_name='是否激活', default=True, null=True)
    isBan = models.BooleanField(verbose_name='是否禁用', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, null=True)
    change_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True, null=True)
    face = models.ImageField(verbose_name='用户头像', default='users-img/admin.png', upload_to='users-img')
    personal_profile = models.CharField(verbose_name='备注', null=True, max_length=100)

    class Meta:
        db_table = "user"
        verbose_name_plural = verbose_name = "用户表"
