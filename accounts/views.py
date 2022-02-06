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
            user.set_password(request.POST.get('password1'))
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
                'joined_since': user.date_joined.strftime('%B %Y'),
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


class ChangePassApi(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        """ Change password """
        response = {
            'success': False,
            'error_message': None,
        }
        user_id = request.POST.get("user_id")
        currentPassword = request.POST.get("current_password")
        newPassword = request.POST.get("new_password")
        confirmPassword = request.POST.get("confirm_password")

        # Get user
        try:
            user = User.objects.get(pk=user_id)
        except:
            response['error_message'] = "User not found."
            return JsonResponse(response)

        username = user.username

        authenticatedUser = authenticate(username=username, password=currentPassword)
        if not authenticatedUser:
            response['error_message'] = "Current password incorrect."
            return JsonResponse(response)

        # Check of new and confirm password are the same
        if newPassword != confirmPassword:
            response['error_message'] = "Passwords do not match."
            return JsonResponse(response)

        # All is good. Set password to new pass
        authenticatedUser.set_password(newPassword)
        authenticatedUser.save()
        response['success'] = True
        return JsonResponse(response)
