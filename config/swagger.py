from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


class BaseOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    '''重写 OpenAPISchemaGenerator 手动为每个路由添加 tag'''

    def get_schema(self, request=None, public=False):
        '''重写父类方法'''
        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "adminlogin",
                "description": "核心功能",
            },
            {
                'name': 'auth',
                'description': '权限管理'
            },
            {
                'name': 'celery',
                'description': '异步任务测试'
            },
            {
                'name': 'confdict',
                'description': '系统字典'
            },
            {
                'name': 'getcode',
                'description': '发送短信验证码'
            },
            {
                'name': 'member',
                'description': '会员管理'
            }
        ]
        return swagger


schema_view = get_schema_view(
    openapi.Info(
        title="Django RESTfulAPI",
        default_version='v3.2',
        description="Ddescription",
        terms_of_service="https://blog.csdn.net/haeasringnar",
        contact=openapi.Contact(email="aeasringnar@163.com"),
        license=openapi.License(name="MIT License"),
    ),
    url="http://127.0.0.1:8000",
    public=True,
    permission_classes=(AllowAny,)
)