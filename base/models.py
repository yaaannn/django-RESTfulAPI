from django.db import models
from soft_delete_it.models import SoftDeleteModel
'''
objects 返回没有删除的所有数据
all_objects 返回所有数据
delete 删除数据，假删
undelete 恢复假删数据
'''


class Group(SoftDeleteModel):
    name = models.CharField(max_length=255,default='',null=True,verbose_name='英文名')
    zhname = models.CharField(max_length=255,default='',null=True,verbose_name='中文名')
    sort = models.IntegerField(default=1,verbose_name='排序')
    created = models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'A_Group_Table'
        verbose_name = '用户组表'
        verbose_name_plural = verbose_name


class User(SoftDeleteModel):
    GENDER_CHOICES = (
        (0, '男'),
        (1, '女'),
        (2, '保密'),
        (3, '未设置'),
    )
    name = models.CharField(max_length=255,default='',verbose_name='用户名')
    phone = models.CharField(max_length=11,verbose_name='用户手机号',null=True)
    email = models.EmailField(default='',verbose_name='用户邮箱',null=True)
    password = models.CharField(max_length=255,default='123456',verbose_name='用户密码')
    gender = models.IntegerField(default='2',verbose_name='用户性别')
    image_url = models.FileField(upload_to='testimage/%Y%m',verbose_name='用户头像',null=True)
    birthday = models.DateField(auto_now_add=True,null=True,verbose_name='用户生日')
    info = models.TextField(null=True,verbose_name='用户信息')
    addr = models.CharField(max_length=255,null=True,verbose_name='用户地址')
    qq = models.CharField(max_length=255,null=True,verbose_name='绑定qq')
    weixin = models.CharField(max_length=255,null=True,verbose_name='绑定微信')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='用户组',null=True)
    sort = models.IntegerField(default=1,verbose_name='排序')
    created = models.DateTimeField(auto_now_add=True,null=True,verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'A_User_Table'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
