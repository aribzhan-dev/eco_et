from django.shortcuts import render
from main.models import *
# Create your views here.




def indexHandler(request):
    return render(request, 'index.html', {})


def corzineHandler(request):
    return render(request, 'corzina.html', {})

def detailsHandler(request):
    return render(request, 'details.html', {})



def that_meetHandler(request):
    return render(request, 'that_meet.html', {})

def custom_404(request):
    return render(request, '404.html', {}, status=404)
