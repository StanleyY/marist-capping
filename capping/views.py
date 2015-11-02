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

def getMaristEqual(request):
  external_subj = request.GET['subject']
  external_number = request.GET['number']
  external = ExternalCourse.objects.get(subject=external_subj, number=external_number)
  mapping = Mapping.objects.get(external_id=external.id)

  #TODO change this get into a filter and use a for loop on QuerySet
  internal = InternalCourse.objects.get(id=mapping.internal_id)
  internal_options = [str(internal.subject) + " " + str(internal.number)]
  return HttpResponse(json.dumps({'courses': internal_options}))

# TODO remove this and redo it properly
def getMajorReq(request):
  majors = {}
  majors_objs = MajorReq.objects.all()
  for major in majors_objs:
    if major.major in majors:
      if major.course not in majors[major.major]:
        majors[major.major].append(major.course)
    else:
      majors[major.major] = [major.course]

  data = json.dumps(majors)
  return HttpResponse(data)
