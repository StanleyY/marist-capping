from django.core.management.base import BaseCommand, CommandError

from capping.models import ExternalCourse, InternalCourse


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
    else:
      self.stdout.write('Unknown model type')
