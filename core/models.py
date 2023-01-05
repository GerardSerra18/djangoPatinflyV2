from django.db import models
from django.utils import timezone


# Create your models here.
class Scooter(models.Model):
    create_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(blank=True, null=True)

    uuid = models.CharField(max_length=64)
    name = models.CharField(max_length=40)
    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)
    battery_level = models.FloatField(default=100.0)
    notification_update = models.DateTimeField(blank=True, null=True)
    meters = models.IntegerField(default=0)
    last_maintenance = models.DateField(blank=True, null=True)
    on_maintenance = models.BooleanField(default=False)
    vacant = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Rent(models.Model):
    date_start = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=64)

    def __str__(self):
        return self.uuid


class ScooterUser(models.Model):
    date_start = models.DateTimeField(blank=True, null=True)
    uuid = models.CharField(max_length=64)

    def __str__(self):
        return self.uuid


class ResponseRent(models.Model):
    code = models.IntegerField(blank=True)
    msg = models.CharField(max_length=64)


class ResponseScooter(models.Model):
    code = models.IntegerField(blank=True)
    msg = models.CharField(max_length=64)

