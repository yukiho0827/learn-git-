from django.db import models


class Department(models.Model):
    depart = models.CharField(verbose_name='部门', max_length=32)

    # def __str__(self):
    #     return self.depart


class Userinfo(models.Model):
    user = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    create_time = models.DateField(verbose_name='入职时间')
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
