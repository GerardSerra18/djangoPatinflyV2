from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from core.models import Scooter, Rent

from rest_framework.authtoken.admin import User
from django.contrib.auth.hashers import check_password


# Create your views here.
def index(request):
    context = {'project_name': 'Patinfly', 'scooters': Scooter.objects.all(), 'rents': Rent.objects.all()}
    return render(request, 'index.html', context)


def static_index(request):
    return render(request, 'static_index.html', context={})


@api_view(['GET'])
def login(request):
    User.objects.create(first_name='Prueba2')
    user = User.objects.get(first_name='Prueba2')

    """username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(first_name='Prueba2')
    except User.DoesNotExist:
        return Response("User does not exist")"""

    token = Token.objects.create(user=user)

    print(token.key)
    return Response(token.key)


@api_view(['GET'])
def rent(request):
    Rent.objects.create(uuid='abc12345')
    rent = Rent.objects.get(uuid='abc12345')
    "token = request.GET.get('token')"
    return Response(rent.uuid)
