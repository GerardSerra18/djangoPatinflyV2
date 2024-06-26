import json
import datetime

from django.shortcuts import render
from django.core.serializers import serialize
from django.utils import timezone

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


def login_firebase(request):
    return render(request, "frontend/login_redirect.html", {})


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
def status(request):
    response = {"status": {"version": version, "build": 1, "update": datetime.datetime.now(), "name": "1-0001"}}
    return Response(response)


@api_view(['GET'])
def rent(request):
    token = request.headers.get('token')
    if isValidToken(token):
        try:
            rents = Rent.objects.filter(user_token=token)
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
    if isValidToken(token):
        try:
            scooters = Scooter.objects.values('name', 'vacant')
            base_response = {"code": status_ok, "msg": "OK", "scooters": scooters,
                             "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "scooters": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "scooters": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


@api_view(['GET'])
def scooter_uuid(request):
    token = request.headers.get('token')
    if isValidToken(token):
        try:
            scooter_uuid = request.GET.get('scooter_uuid')
            scooter = Scooter.objects.filter(uuid=scooter_uuid)
            scooter_filtered = scooter.values('name', 'vacant')
            base_response = {"code": status_ok, "msg": "OK", "scooter": scooter_filtered,
                             "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "scooter": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "scooter": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


@api_view(['GET'])
def start_rent(request):
    token = request.headers.get('token')
    if isValidToken(token):
        try:
            scooter_uuid = request.GET.get('scooter_uuid')
            filtered_scooter = Scooter.objects.filter(uuid=scooter_uuid)
            vacant = filtered_scooter.values('vacant')
            if vacant[0].get('vacant'):
                try:
                    num_rents = Rent.objects.filter(scooter_uuid=scooter_uuid, user_token=token).count()
                except:
                    num_rents = 0

                Rent.objects.create(date_start=timezone.now(), scooter_uuid=scooter_uuid, user_token=token,
                                    num_vacant=num_rents + 1)
                rent = Rent.objects.filter(user_token=token, num_vacant=num_rents + 1)
                Scooter.objects.filter(uuid=scooter_uuid).update(vacant=False)
                response = serialize("json", rent)
                response_json = json.loads(response)
                base_response = {"code": status_ok, "msg": "OK", "rent": response_json,
                                 "timestamp": datetime.datetime.now(), "version": version}
            else:
                base_response = {"code": status_error, "msg": "ERROR SCOOTER NOT AVAILABLE", "rent": [],
                                 "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "SERVER ERROR", "rent": [],
                             "timestamp": datetime.datetime.now(), "version": version}

    else:
        base_response = {"code": status_unauthorized, "msg": "UNAUTHORIZED", "rent": [],
                         "timestamp": datetime.datetime.now(), "version": version}

    return Response(base_response, status=base_response.get("status"))


@api_view(['GET'])
def stop_rent(request):
    token = request.headers.get('token')
    if isValidToken(token):
        try:
            scooter_uuid = request.GET.get('scooter_uuid')
            filtered_scooter = Scooter.objects.filter(uuid=scooter_uuid)
            vacant = filtered_scooter.values('vacant')
            if vacant[0].get('vacant') is False:
                try:
                    num_rents = Rent.objects.filter(scooter_uuid=scooter_uuid, user_token=token).count()
                except:
                    num_rents = 0

                Rent.objects.filter(user_token=token, num_vacant=num_rents).update(date_stop=timezone.now())
                Scooter.objects.filter(uuid=scooter_uuid).update(vacant=True)
                rent = Rent.objects.filter(user_token=token, num_vacant=num_rents)
                response = serialize("json", rent)
                response_json = json.loads(response)
                base_response = {"code": status_ok, "msg": "OK", "rent": response_json,
                                 "timestamp": datetime.datetime.now(), "version": version}
            else:
                base_response = {"code": status_error, "msg": "ERROR SCOOTER AVAILABLE", "rent": [],
                                 "timestamp": datetime.datetime.now(), "version": version}

        except:
            base_response = {"code": status_error, "msg": "INTERNAL SERVER ERROR", "rent": [],
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




