import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response

from capping.models import *
from capping.major_req_types import *

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

def getAllInternalCourses(request):
  internal_course_models = InternalCourse.objects.all();
  li = []
  dump = []
  for ic in internal_course_models:
    li.append({'subject':ic.subject,'number':ic.number})

  dump.append(['courses',li])
  dump = dict(dump)
  return HttpResponse(json.dumps(dump))

def getAllExternalCourses(request):
  external_course_models = ExternalCourse.objects.all();
  li = []
  dump = []
  for ic in external_course_models:
    li.append({'subject':ic.subject,'number':ic.number})

  dump.append(['courses',li])
  dump = dict(dump)
  return HttpResponse(json.dumps(dump))

def getMajors(request):
  majors_models = Majors.objects.all();
  li = []
  dump = []
  for mj in majors_models:
    li.append({'major':mj.major})

  dump.append(['majors',li])
  dump = dict(dump)
  return HttpResponse(json.dumps(dump))

def getMajorReqX(request):
  # Get major from request
  major = request.GET['major']
  # Get all major models from Majors table
  major_model = Majors.objects.get(major = major)

  # Get major id
  major_id = major_model.id

  # Get stat major requirement models from major reqs table
  course_req_models = MajorRequirements.objects.filter(major_id = major_id)

  # Create an empty list for static major reqs
  course_reqs_static = []

  # Cycle through static major req models
  for crm in course_req_models:

    # Get major req from internal course table, internal is and id to interal table
    internal_course_model = InternalCourse.objects.get(id = crm.internal_id )

    # Add a CourseReq object to static list
    course = CourseData(internal_course_model.subject,internal_course_model.number)
    course_reqs_static.append(CourseReqData(course))

  # Get of list items
  of_list_items_models = OfListItems.objects.filter(major_id = major_id)

  # Create a empty list for of list items
  of_list_items = []

  # Cycle through of list items models
  for olim in of_list_items_models:

    # get num selected
    num_sel = olim.number_selected

    # get oid
    _oid = olim.oid

    # Get coursed reqs for this of list items
    of_list_data_models = OfListData.objects.filter(oid = _oid)

    # Create an empty list for of list data course reqs
    of_list_course_reqs = []

    # Cycle through of_list_data models from oflistdata table
    for oldm in of_list_data_models:

      # Get major req from internal course table, internal is and id to interal table
      internal_course_model = InternalCourse.objects.get(id = oldm.internal_id )

      # Create coursedata object for course
      course = CourseData(internal_course_model.subject,internal_course_model.number)

      # Create a course req object for course
      of_list_course_reqs.append(CourseReqData(course))

    # Create a OfListItemData object
    of_list_item_data = OfListItemData(_oid, num_sel, of_list_course_reqs)

    # Add to list of oflistitemdata
    of_list_items.append(of_list_item_data)

  # Get of set items models
  of_set_items_models = OfSetItems.objects.filter(major_id = major_id)

  # Create empty list for of set items
  of_set_items = []

  # Cycle through of set item data models
  for osim in of_set_items_models:

    # Get osid
    _osid = osim.osid

    # Get num selected
    num_sel = osim.number_selected

    # Creat any empty list for course reqs
    course_reqs = []

    # Create an empty list of course req sets
    course_req_sets = []

    # Set last set id
    last_set_id = 0

    # Get of set item data models
    of_set_data_models = OfSetData.objects.filter(osid_id = _osid)

    # Cycle through of set data models
    for osdm in of_set_data_models:

      # Get set id
      set_id = osdm.setid

      # Check if new set id
      if( set_id > last_set_id ):

        # Create a new CourseReqSetData objects
        course_req_set_data = CourseReqSetData(course_reqs,last_set_id)

        # Add list to course req set list
        course_req_sets.append(course_req_set_data)

        # Create a new of set item data object
        #osi = OfSetItemData(_osid, num_sel, course_req_set_data)

        # Add to list of of set items
        #of_set_items.append(osi)

        # Create a new empty list of course reqs
        course_reqs = []

        # Set new last set_id
        last_set_id = set_id

      # Get internal course
      internal_course_model = InternalCourse.objects.get(id = osdm.internal_id )

      # Create a new course and course req object
      course = CourseData(internal_course_model.subject,internal_course_model.number)
      course_reqs.append(CourseReqData(course))

    # Create a new CourseReqSetData objects
    course_req_set_data = CourseReqSetData(course_reqs,set_id)

    # Add to list of course re sets
    course_req_sets.append(course_req_set_data)

    # Create a new of set item data object
    osi = OfSetItemData(_osid, num_sel, course_req_sets)

    # Add to list of of set items
    of_set_items.append(osi)

    # Create a new empty list of course reqs
    course_reqs = []

  # Create major req object
  major_req = MajorRequirementData(major, course_reqs_static, of_list_items, of_set_items)

  # Dump major_req object in JSONN format
  data = json.dumps(major_req.dumpJSON())

  # Respond with JSON object representing total major requirments object
  return HttpResponse(data)


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
  degree_name = request.GET['major'] if request.GET['major'] else "Undecided Major"
  data = [
    ["Institution", "Course", "Marist Course"]
  ]

  selected_courses = request.GET['entries[]'].split(',')

  for i in xrange(0, len(selected_courses), 2):
    data.append([
      "DCC",
      selected_courses[i],    # External Course
      selected_courses[i+1]   # Internal Course
    ])

  # Create the HttpResponse object with the appropriate PDF headers.
  response = HttpResponse(content_type='application/pdf')
  response['Content-Disposition'] = 'attachment; filename="Unoffical Transfer Report.pdf"'

  p = canvas.Canvas(response, pagesize=A4)
  doc_width, doc_height = A4
  y_position = doc_height - 40

  # Drawing the title
  p.setFont("Helvetica-Bold", 36)
  p.drawCentredString(doc_width / 2, y_position, "Unofficial Transfer Report")
  y_position = y_position - 40

  # Draw the degree name
  p.setFont("Helvetica", 16)
  with_index = degree_name.find("WITH")
  if (with_index < 0):
    p.drawCentredString(doc_width / 2, y_position, degree_name)
    y_position = y_position - 20
  else:
    p.drawCentredString(doc_width / 2, y_position, degree_name[0: with_index])
    y_position = y_position - 25
    p.drawCentredString(doc_width / 2, y_position, degree_name[with_index:])
    y_position = y_position - 20


  # Format the data properly
  s = getSampleStyleSheet()
  s = s["BodyText"]
  s.wordWrap = 'CJK'
  data2 = [[Paragraph(cell, s) for cell in row] for row in data]

  # Generate and draw the table on the canvas.
  t = Table(data2)
  style = TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
                    ('VALIGN',(0,0),(0,-1),'TOP'),
                    ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                    ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                    ])
  t.setStyle(style)
  t.wrapOn(p, doc_width / 2, doc_height)
  table_width, table_height = t.wrap(0, 0)
  t.drawOn(p,
           (doc_width / 2) - (table_width / 2) - 15,
           y_position - table_height,
           cm);

  # Finalizes the pdf
  p.showPage()
  p.save()
  return response

def getUser(request):
  username = request.GET['username']
  try:
    user = User.objects.get(username=username)
  except:
    user = None

  if not user:
    user = User(username=username)
    user.save()

  data = serializers.serialize('json', [ user, ])

  return HttpResponse(data)

def getUpdateUser(request):
  username = request.GET['username']
  selected_courses = request.GET['courses']
  selected_major = request.GET['major']
  try:
    user = User.objects.get(username=username)
  except:
    return HttpResponse(status=500)

  user.selected_courses = selected_courses
  user.selected_major = selected_major
  user.save()

  return HttpResponse(status=200)
