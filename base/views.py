from django.db.models import Q
from rest_framework import serializers, status, generics, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# 内置包
import uuid, os, requests, json, re, time, datetime, random, hashlib, xml
# 官方JWT
# from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler ,jwt_response_payload_handler
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# 缓存配置
from django.core.cache import cache
# 下面是定制类导入配置
from .filters import UserFilter
from .permissions import IsAuthenticated, BasePermission
# JWT配置
from .utils import jwt_response_payload_handler,jwt_payload_handler,jwt_encode_handler,google_otp,request_log, VisitThrottle
# from .utils import *
from .authentication import JWTAuthentication
from .models import *
from .serializers import *

'''
name = serializers.CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
name = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
name = serializers.FloatField(max_value=None, min_value=None)
name = serializers.IntegerField(max_value=None, min_value=None)
name = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None)
name = serializers.DateField(format=api_settings.DATE_FORMAT, input_formats=None)
name = serializers.BooleanField()
name = serializers.ListField(child=serializers.IntegerField(min_value=0, max_value=100))
(mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin,generics.GenericAPIView,viewsets.GenericViewSet)
Q(name__icontains=keyword)
'''
# 定pagination类
class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        })




# 登录的view
class LoginInfoSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
class Login(generics.GenericAPIView):
    serializer_class = LoginInfoSerializer
    def post(self,request):
        request_log(request)
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": str(serializer.errors), "errorCode": 4, "data": {}})
            data = (serializer.data)
            username = data.get('username')
            password = data.get('password')
            if username.find('@') == -1 or username.find('.') == -1:
                phone = username
                email = None
            else:
                email = username
                phone = None
            phone_re = re.compile(r'^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\d{8}$', re.IGNORECASE)
            email_re = re.compile(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', re.IGNORECASE)
            user = object
            if phone:
                if not phone_re.match(phone):
                    return Response({"message": "手机号格式错误", "errorCode": 2, "data": {}})
                user = User.objects.filter(phone=phone).first()
                if not user:
                    return Response({"message": "用户不存在", "errorCode": 2, "data": {}})
            if email:
                if not email_re.match(email):
                    return Response({"message": "邮箱格式错误", "errorCode": 2, "data": {}})
                user = User.objects.filter(email=email).first()
                if not user:
                    return Response({"message": "用户不存在", "errorCode": 2, "data": {}})
            if user.password == password:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                data = jwt_response_payload_handler(token,user,request)
                return Response({"message": "登录成功", "errorCode": 0, "data": data})
            else:
                return Response({"message": "密码错误", "errorCode": 0, "data": {}})
        except Exception as e:
            print(e)
            return Response({"message": "未知错误", "errorCode": 1, "data": {}})

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    # captcha = serializers.CharField()
class Register(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    def post(self,request):
        request_log(request)
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response({"message": str(serializer.errors), "errorCode": 4, "data": {}})
            data = (serializer.data)
            username = data.get('username')
            password = data.get('password')
            # captcha = data.get('captcha')
            if username.find('@') == -1 or username.find('.') == -1:
                phone = username
                email = None
            else:
                email = username
                phone = None
            phone_re = re.compile(r'^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\d{8}$', re.IGNORECASE)
            email_re = re.compile(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', re.IGNORECASE)
            if phone:
                if not phone_re.match(phone):
                    return Response({"message": "手机号格式错误", "errorCode": 2, "data": {}})
                account_check = User.objects.filter(phone=phone)
                if account_check:
                    return Response({"message": "用户已经存在", "errorCode": 2})
                account = User()
                account.phone = phone
                # account.password = create_password(password)
                # 明文密码
                account.password = password
                # account.birthday = datetime.date.today()
                account.name = phone + '手机用户'
                # account.group_id = 3
                account.save()
                return Response({"message": "ok", "errorCode": 0})
            if email:
                if not email_re.match(email):
                    return Response({"message": "邮箱格式错误", "errorCode": 2, "data": {}})
                # if not captcha:
                #     return Response({"message": "验证码已过期", "errorCode": 2})
                # if '123456' != captcha:
                #     return Response({"message": "验证码错误", "errorCode": 2})
                account_check = User.objects.filter(email=email)
                if account_check:
                    return Response({"message": "用户已经存在", "errorCode": 2})
                account = User()
                account.email = email
                # account.password = create_password(password)
                # 明文密码
                account.password = password
                account.name = email + '邮箱用户'
                # account.group_id = 3
                account.save()
                return Response({"message": "ok", "errorCode": 0})
        except Exception as e:
            print(e)
            return Response({"message": "未知错误", "errorCode": 1, "data": {}})

class UserInfo(APIView):
    # 加上用户验证 携带正确token时就会有user，否则就是AnonymousUser 就是没有用户的状态
    authentication_classes = (JWTAuthentication,)
    def get(self,request):
        request_log(request)
        try:
            if not request.auth:
                return Response({"message": "请先登录", "errorCode": 2, "data": {}})
            user = User.objects.filter(id=request.user.id).first()
            serializer_user_data = UserSerializer(user)
            json_data = {"message": "ok", "errorCode": 0, "data": {}}
            json_data['data'] = serializer_user_data.data
            return Response(json_data)
        except Exception as e:
            print(e)
            return Response({"message": "未知错误", "errorCode": 1, "data": {}})




class UserViewset(ModelViewSet,viewsets.GenericViewSet):

    # queryset = User.objects.all().order_by('-created')
    # 主要permission要和authentication配合使用才会生效
    authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated,]
    # 频率验证 
    throttle_classes = [VisitThrottle]
    # serializer_class = UserSerializer
    # drf 过滤&搜索&排序
    filter_backends=(DjangoFilterBackend,SearchFilter,OrderingFilter,)
    # 搜索 如何使用 ?search=xx
    search_fields = ('phone', 'name','group__name','group__zhname') # group__name 是搜索外键里面的内容
    # 过滤 如何使用 ?name=xx  phone=xx 使用django自带的方法
    # filter_fields = ('name', 'phone',)
    # 使用django-filter方法
    filter_class = UserFilter
    # 排序 如何使用 ?ordering=xx
    ordering_fields = ('updated',)
    pagination_class = Pagination

    # 动态的根据需求 选择serializers
    def get_serializer_class(self):
        # 创建是修改对应的Serializer 兼容外键的输入
        if self.action == 'create':
            return AddUserSerializer
        return UserSerializer

    # 可以根据需求动态 选择不同 queryset
    def get_queryset(self):
        # print(dir(self))
        print(self.request.user)
        return User.objects.all().order_by('-created')
    
    # 动态的根据访问方式来选择 permissions
    def get_permissions(self):
        if self.action == 'list':
            return []
        else:
            return [IsAuthenticated()]




class GroupViewset(ModelViewSet):
    '''
    测试接口
    '''

    queryset = Group.objects.all().order_by('-created')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BasePermission,]
    # 频率验证 
    throttle_classes = [VisitThrottle]
    serializer_class = GroupSerializer
    # drf 过滤&搜索&排序
    filter_backends=(DjangoFilterBackend,SearchFilter,OrderingFilter,)
    # 搜索 如何使用 ?search=xx
    search_fields = ('zhname', 'name',) # group__name 是搜索外键里面的内容
    # 过滤 如何使用 ?name=xx  phone=xx 使用django自带的方法
    filter_fields = ('name', 'zhname',)
    # 使用django-filter方法
    # filter_class = UserFilter
    # 排序 如何使用 ?ordering=xx
    ordering_fields = ('updated',)
    pagination_class = Pagination


