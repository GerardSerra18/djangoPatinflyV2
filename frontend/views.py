import json

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

from core.models import Scooter, Rent
from rest_framework.authtoken.admin import User

from django.core.serializers import serialize


# Create your views here.
def index(request):
    context = {'project_name': 'Patinfly', 'scooters': Scooter.objects.all(), 'rents': Rent.objects.all()}
    return render(request, 'index.html', context)


def static_index(request):
    return render(request, 'static_index.html', context={})


@api_view(['POST'])
def login(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
            response = "User already exists"

        except:
            User.objects.create_user(username=username, password=password)
            user = User.objects.get(username=username)
            token = Token.objects.create(user=user)
            response = token.key

    except:
        response = "Could not create a Token"

    return Response(response)


@api_view(['GET'])
def validate(request):
    try:
        username = request.headers.get('username')
        token = request.headers.get('token')

        if str(Token.objects.get(key=token).user) == username:
            response = "Valid Token"
        else:
            response = "Invalid Token"

    except:
        response = "Invalid Token"

    return Response(response)


@api_view(['GET'])
def rent(request):
    token = request.headers.get('token')
    if isValidToken(token):
        status = HTTP_200_OK
        try:
            rents = Rent.objects.filter(uuid=token)
            response = serialize("json", rents)
            response = json.loads(response)
        except:
            response = None

    else:
        response = None
        status = HTTP_401_UNAUTHORIZED

    return Response(response, status=status)


def isValidToken(token):
    try:
        Token.objects.get(key=token)
        return True
    except:
        return False
