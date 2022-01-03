"""
Backend URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

extra = {
    'x-logo': {
        'url': '/static/images/Logo_icon.png',
        'backgroundColor': "#FFFFFF",
        'altText': 'Al-Saffar'
    }
}

schema_view = get_schema_view(
    openapi.Info(
        title="Al-Saffar API",
        default_version='v1',
        description="Al-Saffar backend APIs",
        terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email=""),
        license=openapi.License(name="BSD License"),
        **extra
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts'), name='accounts'),
    path('cars/', include(('cars.urls', 'cars'), namespace='cars'), name='cars'),
]
