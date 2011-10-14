from django.core.management.base import BaseCommand
from rapidsms.models import Backend, Connection, Contact
from rapidsms_httprouter.models import Message
from django.conf import settings
from django.db import transaction

class Command(BaseCommand):

    help = """sends messages from all project DBs
    """

    @transaction.commit_manually
    def handle(self, **options):
        while (True):
            for db in settings.DATABASES.keys():
                to_process = MassText.objects.filter()
                to_process = Message.objects.using(db).filter(direction='O',
                                  status__in=['P', 'Q']).order_by('priority', 'status')[0]
