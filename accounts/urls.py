from django.urls import path, re_path
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from .views import AccountCreateApi, TestView

urlpatterns = [
    # Company details and verification stuff
    path('', AccountCreateApi.as_view(), name='account'),
    path('test/', TestView.as_view(), name='test-view'),
]
