from django.urls import path, re_path
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from .views import AccountApi, TestView, LoginAPI, ChangePassApi

urlpatterns = [
    # Company details and verification stuff
    path('', AccountApi.as_view(), name='account'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('changepass/', ChangePassApi.as_view(), name='change-pass'),
    path('test/', TestView.as_view(), name='test-view'),

]
