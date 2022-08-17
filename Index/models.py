from django.db import models


# Create your models here.

# 登录用户
class NewUser(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=10)
    password = models.CharField(verbose_name="密码", max_length=32)
    email = models.CharField(verbose_name="邮箱", max_length=32)
    is_active = models.CharField(verbose_name="激活状态", choices=((1, "True"), (0, "False")), default=0, max_length=4)
    JSESSIONID = models.CharField(verbose_name="jes", max_length=60,default=0)
    route = models.CharField(verbose_name="route", max_length=80,default=0)
    created_time = models.DateTimeField(verbose_name="creat_time", auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name="updated_time", auto_now=True)

    def __str__(self):
        return 'user %s' % self.username
