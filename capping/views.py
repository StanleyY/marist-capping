import json

from django.core import serializers
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from capping.models import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors



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


def getPDF(request):
  print request.GET
  degree_name = "BACHELORS OF SCIENCE IN STUFF"
  data = [
    ["Institution", "Course", "Marist Course"],
    ["DCC", "ART 101", "ART 101"],
    ["DCC", "CHEM 101", "ARTS 101"],
    ["DCC", "03", "SDFSDF"],
    ["DCC", "04", "SDFSDF"],
    ["DCC", "05", "GHJGHJGHJ"],
  ]
  # Create the HttpResponse object with the appropriate PDF headers.
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'attachment; filename="Unoffical Transfer Report.pdf"'

  width, height = A4

  # Utility function
  def coord(x, y, unit=1):
    x, y = x * unit, height -  y * unit
    return x, y

  p = canvas.Canvas(response, pagesize=A4)

  # Drawing the title
  p.setFont("Helvetica-Bold", 36)
  p.drawCentredString(width / 2, height - 40, "Unofficial Transfer Report")
  p.setFont("Helvetica", 20)
  p.drawCentredString(width / 2, height - 80, degree_name)

  style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                      ('VALIGN',(0,0),(0,-1),'TOP'),
                      ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                      ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                      ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                      ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                      ])

  s = getSampleStyleSheet()
  s = s["BodyText"]
  s.wordWrap = 'CJK'
  data2 = [[Paragraph(cell, s) for cell in row] for row in data]
  t=Table(data2)
  t.setStyle(style)
  t.wrapOn(p, width / 2, height)
  t.drawOn(p, *coord(5.3, len(data) + 1, cm));

  # Close the PDF object cleanly, and we're done.
  p.showPage()
  p.save()
  return response
