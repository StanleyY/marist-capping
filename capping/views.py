import json

from django.core import serializers
import json

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

def getMappedExternalData(request):
  all_maps = Mapping.objects.all()
  subjToNums = {}
  for obj in all_maps:
    course = ExternalCourse.objects.get(id=obj.external_id)
    if course.subject in subjToNums:
      if course.number not in subjToNums[course.subject]:
        subjToNums[course.subject].append(course.number)
    else:
      subjToNums[course.subject] = [course.number]
  data = json.dumps(subjToNums)
  return HttpResponse(data)
