from django.db import models

# Create your models here.
class ExternalCourse(models.Model):
  subject = models.CharField(max_length=4)
  number = models.CharField(max_length=4)
  title = models.CharField(max_length=30)


class InternalCourse(models.Model):
  subject = models.CharField(max_length=4)
  number = models.CharField(max_length=4)
  title = models.CharField(max_length=30)
