from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import *
import time, datetime

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name','zhname')



from rest_framework.validators import UniqueValidator
class UserSerializer(serializers.ModelSerializer):
    updated = SerializerMethodField()
    created = SerializerMethodField()
    # group = GroupSerializer(read_only=True) # viewset 使用时无法嵌套创建该数据，需要设置read_only=True防止报错
    group = GroupSerializer()
    class Meta:
        model = User
        fields = ('id','name','phone','email','gender','password','birthday','info','addr','qq','weixin','group','image_url','sort','updated','created')
    
    def get_updated(self,obj):
        if obj.updated:
            return time.strftime('%Y-%m-%d %H:%M',time.strptime(str(obj.updated),'%Y-%m-%d %H:%M:%S.%f'))
        else:
            return ''
    def get_created(self,obj):
        if obj.created:
            return time.strftime('%Y-%m-%d %H:%M',time.strptime(str(obj.created),'%Y-%m-%d %H:%M:%S.%f'))
        else:
            return ''

class AddUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")])
    phone = serializers.CharField(label="手机号", help_text="手机号", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="手机号已经存在")],
                                     error_messages={"required": '手机号不能为空', 'blank': '手机号不能为空', 'null': '手机号不能为空'})
    class Meta:
        model = User
        fields = '__all__'
    
    def get_updated(self,obj):
        if obj.updated:
            return time.strftime('%Y-%m-%d %H:%M',time.strptime(str(obj.updated),'%Y-%m-%d %H:%M:%S.%f'))
        else:
            return ''
    def get_created(self,obj):
        if obj.created:
            return time.strftime('%Y-%m-%d %H:%M',time.strptime(str(obj.created),'%Y-%m-%d %H:%M:%S.%f'))
        else:
            return ''

