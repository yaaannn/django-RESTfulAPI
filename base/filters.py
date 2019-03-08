from django_filters import rest_framework as filters
from .models import *


class UserFilter(filters.FilterSet):
    '''
    用户过滤类
    '''
    name = filters.CharFilter(field_name='name', lookup_expr='icontains') # icontains 表示 包含（忽略大小写）
    group = filters.NumberFilter(field_name='group')  # 外键过滤
    phone = filters.CharFilter(field_name='phone', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['name','phone','group']