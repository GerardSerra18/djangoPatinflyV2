# Create your views here.
from django.contrib.auth.models import User
from rest_framework import generics

from djangoPatinflyV2.urls import UserSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer