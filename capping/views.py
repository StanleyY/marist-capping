import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from capping.models import *


# Create your views here.
def homeView(request):
  return HttpResponse("Hello, world. You're at the polls index.")


def getInternalClass(request):
  obj = InternalCourse.objects.get(id=1)
  data = serializers.serialize('json', [ obj, ])
  return HttpResponse(data)

def getExternalClass(request):
  obj = ExternalCourse.objects.get(id=1999)
  data = serializers.serialize('json', [ obj, ])
  return HttpResponse(data)
