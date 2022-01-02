import json

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView


class AccountCreateApi(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        response = {
            'success': False
        }
        # ('username')
        # ('email')
        # ('password1')
        # ('password2')
        firstName = request.POST.get('fname')
        lastName = request.POST.get('lname')
        signupForm = UserCreationForm(data=request.POST)

        if signupForm.is_valid():
            user: User = signupForm.save(commit=False)
            user.set_password(user.password)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.first_name = firstName
            user.last_name = lastName
            user.save()
            response['success'] = True
        else:
            response['success'] = False

        return JsonResponse(response)
