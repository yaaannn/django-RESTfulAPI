from django.contrib import admin
from django.urls import path, include
# 配置swagger
# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='BaseDjango API')

# 新版swagger
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Base Django API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(r'swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # 官方配置
    # path(r'admin/', admin.site.urls),
    path(r'account/', include('base.urls')),
    # swagger配置
    path(r'docs/', schema_view, name="docs"),
    # path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
