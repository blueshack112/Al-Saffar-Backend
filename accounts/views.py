import json

from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


class AccountApi(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        response = {
            'success': False
        }
        # ('username')
        # ('password1')
        # ('password2')
        firstName = request.POST.get('fname')
        lastName = request.POST.get('lname')
        email = request.POST.get('email')
        signupForm = UserCreationForm(data=request.POST)

        if signupForm.is_valid():
            user: User = signupForm.save(commit=False)
            user.set_password(user.password)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.first_name = firstName
            user.last_name = lastName
            user.email = email
            user.save()
            response['success'] = True
        else:
            response['success'] = False
            response['errors'] = signupForm.errors

        return JsonResponse(response)


class LoginAPI(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        response = {
            'authenticated': False,
            'user_data': None
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        user: User = authenticate(username=username, password=password)

        if user is not None:
            response['authenticated'] = True
            response['user_data'] = {
                'user_id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,

            }
        else:
            response['authenticated'] = False
            response['user_data'] = None
        return JsonResponse(response)


class TestView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        response = {
            'success': True,
        }
        return JsonResponse(response)
