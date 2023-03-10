import os
import sys
import json
import time
import logging
import threading
from decimal import Decimal
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSetMixin
from django.conf import settings
from django.db import transaction
from django.core.cache import caches
from django.forms.models import model_to_dict
from django.http.response import HttpResponseNotFound
from django.db.models import F, Q, Count, Sum, Max, Min
from django.contrib.auth.hashers import check_password, make_password
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_haystack.viewsets import ListModelMixin
from drf_haystack.generics import HaystackGenericAPIView
from drf_haystack.filters import HaystackAutocompleteFilter 
from extensions.JwtToken import JwtToken
from extensions.Pagination import Pagination
from extensions.Throttle import VisitThrottle
from extensions.MyResponse import MyJsonResponse
from extensions.JwtAuth import JwtAuthentication
from extensions.Permission import IsAuthPermission
from .models import *
from .serializers import *
from apps.user.models import User
# from .tasks import *
# from .filters import *
# 不建议导入所有，建议按需导入


class IndexSearchViewSet(ListModelMixin, ViewSetMixin, HaystackGenericAPIView):
    	
	# 指定模型
    index_models = (User, )
    # 指定序列化器
    serializer_class = SearchCollectionAndSpotGoodSerializer
    # 配置检索分页
    pagination_class = Pagination
    filter_backends = [HaystackAutocompleteFilter]