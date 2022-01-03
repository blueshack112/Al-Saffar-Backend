from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
class CarApi:
    def post(self, request: HttpRequest, *args, **kwargs):
        print()
