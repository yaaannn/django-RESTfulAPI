from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from config.swagger import schema_view
from django.conf.urls.static import static


urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('admin/', admin.site.urls),
]
