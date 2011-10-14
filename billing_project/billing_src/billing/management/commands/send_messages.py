from django.core.management.base import BaseCommand
from rapidsms.models import Backend, Connection, Contact
from rapidsms_httprouter.models import Message, MessageBatch
from django.conf import settings
from django.db import transaction
import urllib

class Command(BaseCommand):

    help = """sends messages from all project DBs
    """
    def send_all(self, to_process):
        pass

    @transaction.commit_manually
    def handle(self, **options):
        while (True):
            for db in settings.DATABASES.keys():
                to_process = MessageBatch.objects.using(db).filter(status='P')
                if to_process.count():
                    batch = to_process[0]
                    to_process = batch.messages.using(db).filter(direction='O',
                                  status__in=['P', 'Q']).order_by('priority', 'status')[:100]
                    if to_process.count():
                        self.send_all(to_process)
                    else:
                        batch.status = 'S'
                        batch.save()
                        continue
                else:
                    to_process = Message.objects.using(db).filter(direction='O',
                                      status__in=['P', 'Q']).order_by('priority', 'status')[0]
                    self.send_all([to_process])
