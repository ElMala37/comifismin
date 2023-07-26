from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def accueil(request):
    template = loader.get_template('accueil.html')
    return HttpResponse(template.render())