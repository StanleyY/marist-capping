from django.db import models

class User(models.Model):
  username = models.CharField(primary_key=True, max_length=75)
  password = models.CharField(max_length=30)
  selected_courses = models.TextField()
  selected_major = models.TextField()

class ExternalCourse(models.Model):
  college = models.CharField(max_length=75)
  subject = models.CharField(max_length=4)
  number = models.CharField(max_length=4)
  title = models.CharField(max_length=30)

  class Meta:
    unique_together = (('college', 'subject', 'number'), )

class InternalCourse(models.Model):
  subject = models.CharField(max_length=4)
  number = models.CharField(max_length=4)
  title = models.CharField(max_length=30)
  # Edit
  class Meta:
    unique_together = (('subject','number'),)
  #--

class Mapping(models.Model):
  external = models.ForeignKey('ExternalCourse')
  internal = models.ForeignKey('InternalCourse')

  class Meta:
    unique_together = (('external', 'internal'),)

# Major Requirements Models

# OneLuminare edit
class Majors(models.Model):
  major = models.CharField(max_length=100)

class MajorRequirements(models.Model):
  major = models.ForeignKey('Majors')
  internal = models.ForeignKey('InternalCourse')

  class Meta:
    unique_together = (('major','internal'),)

class OfListItems(models.Model):
  oid = models.IntegerField(primary_key=True)
  major = models.ForeignKey('Majors')
  number_selected = models.IntegerField()

class OfListData(models.Model):
  oid = models.ForeignKey('OfListItems')
  internal = models.ForeignKey('InternalCourse')

  class Meta:
    unique_together = (('oid','internal'),)

class OfSetItems(models.Model):
  osid = models.IntegerField(primary_key=True)
  major = models.ForeignKey('Majors')
  number_selected = models.IntegerField()
  set_size = models.IntegerField()

class OfSetData(models.Model):
  osid = models.ForeignKey('OfSetItems')
  setid = models.IntegerField()
  internal = models.ForeignKey('InternalCourse')

  class Meta:
    unique_together = (('osid','setid','internal'),)
#--
