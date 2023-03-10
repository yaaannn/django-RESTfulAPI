from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from extensions.BaseModel import BaseModel
from django.utils.translation import gettext_lazy


class Group(BaseModel):
    group_type_choices = (
        ('SuperAdmin', '超级管理员'),
        ('Admin', '管理员'),
        ('NormalUser', '普通用户'),
    )
    group_type = models.CharField(max_length=128, choices=group_type_choices, verbose_name='用户组类型')
    group_type_cn = models.CharField(max_length=128, verbose_name='用户组类型_cn')

    class Meta:
        db_table = 'a_group'
        verbose_name = '用户组表'
        verbose_name_plural = verbose_name


class User(BaseModel):
    # 管理员时使用账户密码登录
    class Suit(models.TextChoices):
        female = 'female', gettext_lazy('女')
        male = 'male', gettext_lazy('男')
        privacy = 'privacy', gettext_lazy('保密')
        
        
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=True, verbose_name='用户组')
    username = models.CharField(max_length=32, default='', blank=True, verbose_name='用户账号')
    password = models.CharField(max_length=255, default='',blank=True, verbose_name='用户密码')
    mobile = models.CharField(max_length=16, default='', blank=True, verbose_name='手机号')
    email = models.EmailField(default='', blank=True, verbose_name='邮箱')
    nick_name = models.CharField(max_length=32, default='', blank=True, verbose_name='昵称')
    region = models.CharField(max_length=255, default='', blank=True, verbose_name='地区')
    avatar_url = models.CharField(max_length=255, default='', blank=True, verbose_name='头像')
    gender = models.CharField(max_length=64, choices=Suit.choices, default='privacy', verbose_name='性别')
    birth_date = models.CharField(max_length=10, default='', blank=True, verbose_name='生日')
    is_freeze = models.BooleanField(default=False, verbose_name='是否冻结/是否封号')
    bf_logo_time = models.BigIntegerField(default=0, verbose_name='上次登录时间戳')
    jwt_version = models.IntegerField(default=0, verbose_name='jwt token版本')
    # is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    # group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name='用户组')
    # 组权分离后 当有权限时必定为管理员类型用户，否则为普通用户
    # auth = models.ForeignKey(Auth, on_delete=models.PROTECT, null=True, blank=True, verbose_name='权限组') # 当auth被删除时，当前user的auth会被保留，但是auth下的auth_permissions会被删除，不返回
    

    class Meta:
        db_table = 'a_user_table'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name