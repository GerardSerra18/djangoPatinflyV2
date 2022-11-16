from django.shortcuts import render

from core.models import Scooter


# Create your views here.
# Prueba

def index (request):

    context = {'project_name': 'Patinfly', 'scooters': Scooter.objects.all()}
    return render(request, 'index.html', context)

def static_index(request):
    return render(request, 'static_index.html', context={})