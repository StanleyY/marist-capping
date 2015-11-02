from django.core.management.base import BaseCommand, CommandError

from capping.models import *


class Command(BaseCommand):
  args = '<filename model_name>'
  help = 'Populates the database'

  def handle(self, *args, **options):
    filename = args[0]
    model_name = args[1]

    if model_name == 'dcc':
      with open(filename, 'r') as f:
        for line in f:
          # I only split on the first two commas because titles sometime have
          # commas in them.
          subject, num, title = line.strip().replace('"', '').split(',', 2)
          model = ExternalCourse(subject=unicode(subject, errors='ignore'),
                                 number=unicode(num, errors='ignore'),
                                 title=unicode(title, errors='ignore'))
          model.save()
      self.stdout.write('Finished writing to DCC courses')
    elif model_name == 'marist':
      with open(filename, 'r') as f:
        for line in f:
          # I only split on the first two commas because titles sometime have
          # commas in them.
          subject, num, title = line.strip().replace('"', '').split(',', 2)
          model = InternalCourse(subject=unicode(subject, errors='ignore'),
                                 number=unicode(num, errors='ignore'),
                                 title=unicode(title, errors='ignore'))
          model.save()
      self.stdout.write('Finished writing to Marist courses')
    elif model_name == 'mapping':
      broken = 0
      working = 0
      with open(filename, 'r') as f:
        for line in f:
          external_subj, external_num, internal_subj, internal_num = line.strip().replace('"', '').split(',')
          try:
            external_course = ExternalCourse.objects.get(subject=unicode(external_subj, errors='ignore'),
                                                         number=unicode(external_num, errors='ignore'))
            internal_course = InternalCourse.objects.get(subject=unicode(internal_subj, errors='ignore'),
                                                       number=unicode(internal_num, errors='ignore'))
            mapping = Mapping(external=external_course,
                              internal=internal_course)
            mapping.save()
            working += 1
          except:
            broken += 1
            self.stdout.write("No match for: %s, %s, %s, %s" %
                (external_subj, external_num, internal_subj, internal_num))

      self.stdout.write("Inserted %d" % working)
      self.stdout.write("Failed %d" % broken)
    elif model_name == 'major_req':
      with open(filename, 'r') as f:
        for line in f:
          major, course_name, course_num = line.strip().replace('"', '').rsplit(',', 2)
          major_req = MajorReq(major=unicode(major, errors='ignore'),
                               course=unicode(course_name + " " + course_num, errors='ignore'))
          major_req.save()
    else:
      self.stdout.write('Unknown model type')
