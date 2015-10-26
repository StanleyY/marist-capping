import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from capping.models import *


# Create your views here.
def homeView(request):
  return render_to_response('index.html')


def getInternalClass(request):
  obj = InternalCourse.objects.order_by('?').first()
  data = serializers.serialize('json', [ obj, ])
  return HttpResponse(data)

def getExternalClass(request):
  obj = ExternalCourse.objects.order_by('?').first()
  data = serializers.serialize('json', [ obj, ])
  return HttpResponse(data)
