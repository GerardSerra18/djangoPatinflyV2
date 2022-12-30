"""djangoPatinflyV2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from frontend import views

from core.models import Scooter, Rent, ScooterUser
from djangoPatinflyV2 import settings
from frontend import views as frontend_views
from rest_framework import serializers, viewsets, routers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ScooterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Scooter
        fields = ['uuid', 'name', 'longitude', 'latitude', 'battery_level', 'notification_update', 'meters',
                  'last_maintenance', 'on_maintenance', 'vacant']


class ScooterViewSet(viewsets.ModelViewSet):
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer


class RentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rent
        fields = ['date_start', 'uuid']


class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer


class ScooterUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ScooterUser
        fields = ['date_start', 'uuid']


class ScooterUserViewSet(viewsets.ModelViewSet):
    queryset = ScooterUser.objects.all()
    serializer_class = ScooterUserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'scooter', ScooterViewSet)
router.register(r'scooter_user', ScooterUserViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls')),
                  path('', include(router.urls)),
                  path('index', frontend_views.index),
                  path('static_index', frontend_views.static_index),
                  path('endpoints/login', views.login),
                  path('endpoints/rent', views.rent)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

