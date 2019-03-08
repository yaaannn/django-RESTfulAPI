from django.conf.urls import url
from django.urls import path, include
from base import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# 用户
router.register(r'user', views.UserViewset, base_name='users')
router.register(r'group', views.GroupViewset, base_name='group')

urlpatterns = [
    path('', include(router.urls)),
    path('login',views.Login.as_view(),name='login'),
    path('register',views.Register.as_view(),name='register'),
    path('userinfo',views.UserInfo.as_view(),name='userinfo'),
]