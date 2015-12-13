import json
# Classes


class MajorRequirementData:
  """ Defines total major requirement data. Contains list of CourseReqs,OfListItems,and OfSetItems. """
  def __init__(self,major,course_reqs,of_list_items,of_set_items):
    self.major = major
    self.course_reqs = []
    self.of_list_items = []
    self.of_set_items = []
    for cr in course_reqs:
      self.course_reqs.append(cr)
    for oli in of_list_items:
      self.of_list_items.append(oli)
    for osi in of_set_items:
      self.of_set_items.append(osi)

  def dumpJSON(self):
    dump = []
    dump.append(['major',self.major])
    li = []
    id = 0
    for cr in self.course_reqs:
      d = cr.dumpJSON()
      #li.append([id,d])
      li.append(d)
      id += 1
    #dump.append(['courses',dict(li)])
    dump.append(['courses',li])
    li = []
    id = 0
    for oli in self.of_list_items:
      d = oli.dumpJSON()
      #li.append([id,d])
      li.append(d)
      id += 1
    #dump.append(['oflistitems',dict(li)])
    dump.append(['oflistitems',li])
    li = []
    id = 0
    for osi in self.of_set_items:
      d = osi.dumpJSON()
      #li.append([id,d])
      li.append(d)
      id += 1
    #dump.append(['ofsetitems',dict(li)])
    dump.append(['ofsetitems',li])
    dump = dict(dump)
    return dump

class OfSetItemData():
  """ Contrain of set item data. """
  def __init__(self,osid,selected,course_req_sets):
    self.osid = osid
    self.number_selected = selected
    self.completed = False
    self.selected = 0
    self.coursesets = []
    for cs in course_req_sets:
      self.coursesets.append(cs)

  def setCourseReq(self,coursereq):
    i = 0
    found = False
    fcrs = 'null'
    noinc = False
    while ((i < len(self.coursesets)) and (found != True)):
      for crs in self.coursesets[i].courses:
        if( crs.internal_course == coursereq.internal_course):
          if( crs.isCompleted() == True ):
            noinc = True
          fcrs = self.coursesets[i]
          crs.external_course = coursereq.external_course
          found = True
      i += 1

    if ( found ):
      if( fcrs != 'null' ):
        if( fcrs.isCompleted() == True):
          if( noinc != True):
            self.selected += 1
          if( self.selected >= self.number_selected):
            self.completed = True
          else:
            self.completed = False

    return found

  def clearCourseReq(self,course):
    i = 0
    found = False
    fcrs = 'null'
    while (i < len(self.coursesets)) and (found != True):
      for crs in self.coursesets[i].courses:
        if( crs.internal_course == course):
          crs.clearExCourse()
          found = True
          fcrs = self.coursesets[i]
      i += 1

    if( found ):
      if( fcrs.isCompleted() != True ):
        self.selected -= 1
        if( self.selected >= self.number_selected):
          self.completed = True
        else:
          self.completed = False

    return found

  def clearAllCourseReq(self):
    for crs in self.coursesets:
      for cr in crs.courses:
        cr.clearExCourse()

    self.selected = 0
    self.completed = False

  def dumpJSON(self):
    dump = []
    dump.append(['osid',self.osid])
    dump.append(['number_selected',self.number_selected])
    dump.append(['completed',self.completed])
    dump.append(['selected',self.selected])
    li = []
    id = 0
    for crs in self.coursesets:
      d = crs.dumpJSON()
      #li.append([id,d])
      li.append(d)
      id += 1
    #dump.append(['coursereqsets',dict(li)])
    dump.append(['coursereqsets',li])
    dump = dict(dump)
    return dump



class CourseReqSetData:
  """ Contains a course req set for CourseSetData class. """
  def __init__(self,courses,setid):
    self.courses = []
    self.setid = setid
    for cr in courses:
      self.courses.append(cr)

  def setCourseReq(self,coursereq):
    found = False
    i = 0
    while (i < len(self.courses)) and (found != True):
      if( self.courses[i].internal_course == coursereq.internal_course):
        self.courses[i].external_course = coursereq.external_course
        found = True
      i += 1
    return found

  def clearCourseReq(self,course):
    found = False
    i = 0
    while (i < len(self.courses)) and (found != True):
      if( self.courses[i].internal_course == course):
        self.courses[i].clearExCourse()
        found = True
      i += 1
    return found

  def isCompleted(self):
    comp = True
    for cr in self.courses:
      if( cr.isCompleted() != True ):
        comp = False

    return comp

  def dumpJSON(self):
    dump = []
    dump.append(['setid',self.setid])
    li = []
    id = 0
    for crs in self.courses:
      d = crs.dumpJSON()
      #li.append([id,d])
      li.append(d)
      id += 1
    #dump.append(['coursereqs',dict(li)])
    dump.append(['coursereqs',li])
    dump = dict(dump)
    return dump




class OfListItemData():
  """ Contains of list item data. """
  def __init__(self,liOid,liSel,liCourseReqs):
    self.oid = liOid
    self.number_selected = liSel
    self.completed = False
    self.selected = 0
    self.courses = []
    for cr in liCourseReqs:
      self.courses.append(cr)

  def setCourseReq(self,coursereq):
    i = 0
    found = False
    noinc = False
    while (i < len(self.courses)) and (found != True):
      if( self.courses[i].internal_course == coursereq.internal_course):
        if( self.courses[i].isCompleted() == True ):
          noinc = True
        self.courses[i].external_course = coursereq.external_course
        found = True
      i += 1

    if( found ):
      if( noinc != True):
        self.selected += 1
      if( self.selected >= self.number_selected):
        self.completed = True
      else:
        self.completed = False

    return found

  def clearCourseReq(self,course):
    i = 0
    found = False
    while (i < len(self.courses)) and (found != True):
      if( self.courses[i].internal_course == course):
        self.courses[i].clearExCourse()
        found = True
      i += 1

    if( found ):
      self.selected -= 1
      if( self.selected >= self.number_selected):
        self.completed = True
      else:
        self.completed = False

    return found

  def clearAllCourseReq(self):
    for cr in self.courses:
      cr.clearExCourse()

    self.selected = 0
    self.completed = False

  def dumpJSON(self):
    dump = []
    dump.append(['oid',self.oid])
    dump.append(['number_selected',self.number_selected])
    dump.append(['completed',self.completed])
    dump.append(['selected',self.selected])
    li = []
    id = 0
    for cr in self.courses:
      d = cr.dumpJSON()
      #li.append([id,d])
      li.append(d)
      id += 1
    #dump.append(['coursesreqs',dict(li)])
    dump.append(['coursereqs',li])
    dump = dict(dump)
    return dump


class CourseReqData:
  """ Course Requirement Data, ex and internal courses. External course is 'null' when not fulfilled."""
  def __init__(self,course):
    self.internal_course = course
    self.external_course = 'null'
    self.fulfilled = False

  def isCompleted(self):
    ret = True
    if( self.external_course == 'null'):
      ret = False
    return ret

  def setExternalCourse(self,course):
    self.external_course = course

  def clearExCourse(self):
    self.external_course = 'null'

  def dumpJSON(self):
    intcr = self.internal_course.dumpJSON()
    if( self.external_course == 'null'):
      excr = {}
    else:
      excr = self.external_course.dumpJSON()
    dump = { 'internal_course': intcr, 'external_course': excr}
    return dump

class CourseData:
  """ Contains class data, subject and number. """
  def __init__(self,sub,num):
    self.subject = sub
    self.number = num

  def __eq__(self,other):
    if( isinstance(other,self.__class__)):
      return (self.subject == other.subject) and (self.number == other.number)
    else:
      return False

  def __nq__(self,other):
    return not self.__eq__(other)

  def dumpJSON(self):
    return self.__dict__


# Test Data
cd1 = CourseData('CMPT',330)
cd2 = CourseData('CS',301)
cd3 = CourseData('BIOL',440)
cd4 = CourseData('BIO',375)
lic1 = [cd1,cd2]
lic2 = [cd3,cd4]
crd1 = CourseReqData(cd1)
crd2 = CourseReqData(cd3)
licrd1 = [crd1,crd2]
oli1 = OfListItemData(0,1,licrd1)
crd3 = CourseReqData(cd3)
crd3.setExternalCourse(cd4)
oli1.setCourseReq(crd3)
crd3 = CourseReqData(cd2)
crd4 = CourseReqData(cd4)
licrd2 = [crd3,crd4]
crsd1 = CourseReqSetData(licrd1,0)
crsd2 = CourseReqSetData(licrd2,1)
licrsd = [crsd1,crsd2]
osid1 = OfSetItemData(0,1,licrsd)
cd5 = CourseData('REQ',100)
cd6 = CourseData('REQ',200)
cd7 = CourseData('REQ',300)
cd8 = CourseData('REQ',400)
crdx1 = CourseReqData(cd1)
crdx1.setExternalCourse(cd5)
crdx2 = CourseReqData(cd2)
crdx2.setExternalCourse(cd6)
crdx3 = CourseReqData(cd3)
crdx3.setExternalCourse(cd7)
crdx4 = CourseReqData(cd4)
crdx4.setExternalCourse(cd8)
cr1 = CourseReqData(cd1)
cr2 = CourseReqData(cd2)
cr3 = CourseReqData(cd3)
cr4 = CourseReqData(cd4)
licrd3 = [cr1,cr2]
licrd4 = [cr3,cr4]
cs1 = CourseReqSetData(licrd3,0)
cs2 = CourseReqSetData(licrd4,1)
lics1 = [cs1,cs2]
osid2 = OfSetItemData(0,1,lics1)
cd9 = CourseData('TEST',200)
crdx5 = CourseReqData(cd2)
crdx5.setExternalCourse(cd9)
osid2.setCourseReq(crdx1)
osid2.setCourseReq(crdx2)
