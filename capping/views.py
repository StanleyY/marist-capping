import json

from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def homeView(request):
  return HttpResponse("Hello, world. You're at the polls index.")


def getClass(request):
  data = json.dumps({'key': "stuff"})
  return HttpResponse(data)
