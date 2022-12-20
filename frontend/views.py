from django.shortcuts import render

from core.models import Scooter, Rent


# Create your views here.

def index (request):

    context = {'project_name': 'Patinfly', 'scooters': Scooter.objects.all(), 'rents': Rent.objects.all()}
    return render(request, 'index.html', context)

def static_index(request):
    return render(request, 'static_index.html', context={})