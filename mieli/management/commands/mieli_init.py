from mieli.cli import MieliCommand
from django.contrib.sites.models import Site

class Command(MieliCommand):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.register_option(
            '--domain',
            dest='domain',
            help='Organization\'s domain',
            required=True)

    def invoke(self, *args, **options):
        sites = Site.objects.all()
        for site in sites:
            site.delete()
