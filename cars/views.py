from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from rest_framework import status

from cars.models import Car


class CarApi(View):
    def post(self, request: HttpRequest, *args, **kwargs):
        """ Create/Register a car """
        response = {
            'success': False,
            'car_id': None,
            'error_message': None
        }

        # Read data
        brand = request.POST.get('brand')
        make = request.POST.get('make')
        model = request.POST.get('model')
        year = int(request.POST.get('year'))
        user_id = request.POST.get('user_id')
        capacity = int(request.POST.get('capacity'))

        # Make sure the user doesn't already have a car
        try:
            user = User.objects.get(pk=user_id)
        except:
            response['error_message'] = "User could not be identified."
            return JsonResponse(response)

        if user is None:
            response['error_message'] = "User could not be identified."
            return JsonResponse(response)

        temp = Car.objects.filter(owner_id=user_id)
        if len(temp) > 0:
            response['error_message'] = "You have already registered a car."
            return JsonResponse(response)

        # Save model
        newCar = Car()
        newCar.brand = brand
        newCar.make = make
        newCar.model = model
        newCar.year = year
        newCar.owner_id = user
        newCar.capacity = capacity
        newCar.approved = True
        newCar.condition = 4
        newCar.save()

        response['success'] = True
        response['car_id'] = newCar.id
        return JsonResponse(response)

    def get(self, request: HttpRequest, *args, **kwargs):
        """ Get a car using car id or user id """
        response = {
            'success': False,
            'car_id': None,
            'error_message': None,
            'car_data': None
        }
        # Read data
        user_id = request.GET.get('user_id')
        car_id = request.GET.get('car_id')

        if not car_id and not user_id:
            response['error_message'] = "Bad request."
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

        # Find car using car_id
        if car_id:
            car = None
            try:
                car = Car.objects.get(pk=car_id)
            except:
                pass

            if car:
                response['success'] = True
                response['car_id'] = car.pk
                response['car_data'] = {
                    'brand': car.brand,
                    'make': car.make,
                    'model': car.model,
                    'year': car.year,
                    'capacity': car.capacity,
                    'condition': car.condition,
                    'approved': car.approved,
                }
                return JsonResponse(response)

        # Try through user id
        if user_id:
            cars = Car.objects.filter(owner_id=user_id)
            if len(cars) > 0:
                car = cars[0]
                response['success'] = True
                response['car_id'] = car.pk
                response['car_data'] = {
                    'brand': car.brand,
                    'make': car.make,
                    'model': car.model,
                    'year': car.year,
                    'capacity': car.capacity,
                    'condition': car.condition,
                    'approved': car.approved,
                }
                return JsonResponse(response)

        response['error_message'] = "Car details not found."
        return JsonResponse(response)


class DeleteCarApi(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        """ Delete a car using car id or user id """
        response = {
            'success': False,
            'error_message': None,
        }
        # Read data
        user_id = request.GET.get('user_id')
        car_id = request.GET.get('car_id')

        if not car_id and not user_id:
            response['error_message'] = "Bad request."
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST)

        # Find car using car_id
        if car_id:
            car = None
            try:
                car = Car.objects.get(pk=car_id)
            except:
                pass

            if car:
                car.delete()
                response['success'] = True
                return JsonResponse(response)

        # Try through user id
        if user_id:
            cars = Car.objects.filter(owner_id=user_id)
            if len(cars) > 0:
                car = cars[0]
                car.delete()
                response['success'] = True
                return JsonResponse(response)

        response['error_message'] = "Car not found."
        return JsonResponse(response)
