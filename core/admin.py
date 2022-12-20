from django.contrib import admin

# Register your models here.

from core.models import Scooter, ScooterUser, Rent


class ScooterAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid', 'latitude', 'longitude', 'vacant', 'on_maintenance']
    list_filter = ['vacant', 'on_maintenance']


admin.site.register(Scooter, ScooterAdmin)


class RentAdmin(admin.ModelAdmin):
    list_display = ['date_start', 'uuid']


admin.site.register(Rent, RentAdmin)


class ScooterUserAdmin(admin.ModelAdmin):
    list_display = ['date_start', 'uuid']


admin.site.register(ScooterUser, ScooterUserAdmin)
