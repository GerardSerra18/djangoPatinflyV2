import json
import datetime

from django.shortcuts import render
from django.core.serializers import serialize

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.authtoken.admin import User

from core.models import Scooter, Rent

# Create your views here.
version = "1.0"
status_ok = HTTP_200_OK
status_unauthorized = HTTP_401_UNAUTHORIZED
status_error = HTTP_500_INTERNAL_SERVER_ERROR


def index(request):
    context = {'project_name': 'Patinfly', 'scooters': Scooter.objects.all(), 'rents': Rent.objects.all()}
    return render(request, 'index.html', context)


def static_index(request):
    return render(request, 'static_index.html', context={})


@api_view(['POST'])
def signin(request):
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
        try:
            rents = Rent.objects.filter(uuid=token)
            response = serialize("json", rents)
            response_json = json.loads(response)
            base_response = {"code": status_ok, "msg": "OK", "rent": response_json,
                             "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "rent": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "rent": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


@api_view(['GET'])
def scooter(request):
    token = request.headers.get('token')
    print(token)
    if isValidToken(token):
        try:
            scooters = Scooter.objects.values('name', 'vacant')
            base_response = {"code": status_ok, "msg": "OK", "Scooters": scooters,
                             "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "Scooters": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "Scooters": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


@api_view(['GET'])
def scooter_uuid(request):
    token = request.headers.get('token')
    if isValidToken(token):
        try:
            scooter_uuid = request.GET.get('scooter_uuid')
            print(scooter_uuid)
            scooter = Scooter.objects.filter(uuid=scooter_uuid)
            print(scooter)
            scooter_filtered = scooter.values('name', 'vacant')
            print(scooter_filtered)
            base_response = {"code": status_ok, "msg": "OK", "Scooter": scooter_filtered,
                             "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "Scooter": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "Scooter": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


@api_view(['POST'])
def start_rent(request):
    token = request.headers.get('token')
    if isValidToken(token):
        try:
            # TODO: CREAR LÓGICA PARA ALGUILAR UN SCOOTER
            rents = Rent.objects.filter(uuid=token)
            response = serialize("json", rents)
            response_json = json.loads(response)
            base_response = {"code": status_ok, "msg": "OK", "rent": response_json,
                             "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "rent": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "rent": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


@api_view(['POST'])
def stop_rent(request):
    token = request.headers.get('token')
    if isValidToken(token):
        try:
            # TODO: CREAR LÓGICA PARA DETENER EL ALGUILER DE UN SCOOTER
            rents = Rent.objects.filter(uuid=token)
            response = serialize("json", rents)
            response_json = json.loads(response)
            base_response = {"code": status_ok, "msg": "OK", "rent": response_json,
                             "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "rent": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "rent": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


def isValidToken(token):
    try:
        Token.objects.get(key=token)
        return True
    except:
        return False
