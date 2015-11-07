import json

from django.core import serializers
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from capping.models import *

# OneLuminare
from major_req_types import *


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

def getMajorReq(request):
	# Get major from request
	major = request.GET['major']
	
	# Get all major models from Majors table
	major_model = Majors.objects.get(major = major)
	
	# Get major id
	major_id = major_model.id
	
	# Get stat major requirement models from major reqs table
	course_req_models = MajorRequirements.objects.get(major = major_id)
	
	# Create an empty list for static major reqs
	course_reqs_static = []
	
	# Cycle through static major req models
	for crm in course_req_models:
	
		# Get major req from internal course table, internal is and id to interal table
		internal_course_model = InternalCourse.objects.get(internal = crm.internal )
		
		# Add a CourseReq object to static list
		course = CourseData(internal_course_model.subject,internal_course_model.number)
		course_reqs_static.append(CourseReqData(course))
		
	# Get of list items
	of_list_items_models = OfListItems.objects.get(major = major_id)
	
	# Create a empty list for of list items
	of_list_items = []
		
	# Cycle through of list items models
	for olim in of_list_items_models:
	
		# get num selected
		num_sel = olim.number_selected
		
		# get oid
		_oid = olim.oid
		
		# Get coursed reqs for this of list items
		of_list_data_models = OfListData.objects.get(oid = _oid)
		
		# Create an empty list for of list data course reqs
		of_list_course_reqs = []
		
		# Cycle through of_list_data models from oflistdata table
		for oldm in of_list_data_models:
		
			# Get major req from internal course table, internal is and id to interal table
			internal_course_model = InternalCourse.objects.get(internal = oldm.internal )
			
			# Create coursedata object for course
			course = CourseData(internal_course_model.subject,internal_course_model.number)
			
			# Create a course req object for course
			of_list_course_reqs.append(CourseReqData(course))
			
		# Create a OfListItemData object
		of_list_item_data = OfListItemData(_oid, num_sel, of_list_course_reqs)
		
		# Add to list of oflistitemdata 
		of_list_items.append(of_list_item_data)
		
	# Get of set items models
	of_set_items_models = OfSetItems.objects.get(major = major_id)
	
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
		
		# Set last set id
		last_set_id = 0
		
		# Get of set item data models
		of_set_data_models = OfSetData.objects.get(major = major_id)
		
		# Cycle through of set data models
		for osdm in of_set_data_models:
		
			# Get set id
			set_id = osdm.setid
		
			# Check if new set id
			if( set_id > last_set_id ):
			
				# Create a new CourseReqSetData objects
				course_req_set_data = CourseReqSetData(course_reqs,last_set_id)
			
				# Create a new of set item data object
				osi = OfSetItemData(_osid, num_sel, course_req_set_data)
				
				# Add to list of of set items
				of_set_items.append(osi)
				
				# Create a new empty list of course reqs
				course_reqs = []
				
				# Set new last set_id
				last_set_id = set_id
				
			# Get internal course 
			internal_course_model = InternalCourse.objects.get(internal = osdm.internal )
				
			# Create a new course and course req object
			course = CourseData(internal_course_model.subject,internal_course_model.number)
			course_reqs.append(CourseReqData(course))
			
		# Create a new CourseReqSetData objects
		course_req_set_data = CourseReqSetData(course_reqs,set_id)
			
		# Create a new of set item data object
		osi = OfSetItemData(_osid, num_sel, course_req_set_data)
				
		# Add to list of of set items
		of_set_items.append(osi)
				
		# Create a new empty list of course reqs
		course_reqs = []
		
	# Create major req object
	major_req = MajorRequirementData(major, course_reqs_static, of_list_items, of_set_items)
	
	# Dump major_req object in JSON format
	data = json.dumps(major_req)
	
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
