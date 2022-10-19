from django.shortcuts import render

from core.models import Scooter


# Create your views here.

def index (request):

    context = {'project_name': 'Patinfly', 'scooters': Scooter.objects.all()}
    return render(request, 'index.html', context)
