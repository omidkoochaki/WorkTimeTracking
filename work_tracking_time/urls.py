"""work_tracking_time URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.conf.urls import url
from django.urls import path, include, re_path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# schema_view = get_swagger_view(title='Pastebin API')

schema_view = get_schema_view(
   openapi.Info(
      title="Working Time Tracker API",
      default_version='v 0.1',
      description="This API is made by Omid.koochaki@gmail.com.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="omid.koochaki@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('time_tracker.urls')),
    path('auth/', include('time_tracking_auth.urls')),
    path(r'', include_docs_urls(title='Working Time Tracker API')),
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'swager', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('docs', schema_view)
    ]
