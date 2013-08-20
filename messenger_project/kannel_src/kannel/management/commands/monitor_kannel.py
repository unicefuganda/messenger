#!/usr/bin/env python
from xml.dom import minidom
import urllib2
import smtplib
from optparse import make_option
from multiprocessing import Process
import time
from rapidsms.log.mixin import LoggerMixin

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.mail import send_mail


class Command(BaseCommand, LoggerMixin):
    help = "monitor the kannel smsc links  and send a email notification if one of them is down "

    def get_status(self):
        KANNEL_HOST = getattr(settings, 'KANNEL_HOST', 'http://localhost:13000/status.xml')
        recipients = getattr(settings, 'ADMINS', None)
        if recipients:
            recipients = [email for name, email in recipients]
        else:
            recipients = []
        mgr = getattr(settings, 'MANAGERS', None)
        if mgr:
            for email in mgr:
                recipients.append(email)
        others = getattr(settings, 'CHANNEL_CONTACTS', {})
        try:
            response = urllib2.urlopen(KANNEL_HOST)
        except urllib2.URLError, e:
            if not hasattr(e, "code"):
                raise
            print e
        if response.code == 200:
            raw_data = response.read()
            xmldoc = minidom.parseString(raw_data)
            smsc_list = xmldoc.getElementsByTagName('smsc')
            for smsc in smsc_list:
                if smsc.getElementsByTagName('status')[0].childNodes[0].data.split(" ")[0] != "online":
                    smsc_name = smsc.getElementsByTagName('id')[0].childNodes[0].data
                    if smsc_name in getattr(settings, 'UNMONITORED_SMSCS', ['fake']):
                        continue
                    if smsc_name in others:
                        recipients += others[smsc_name]

                    subject = smsc_name + " is down!!"
                    message = smsc_name + " is down!! " + \
                    " more info: %s" % KANNEL_HOST

                    send_mail(subject, message, settings.EMAIL_HOST_USER,
                    recipients, fail_silently=False)
        else:
            subject = "Kannel id down"
            send_mail(subject, subject, settings.EMAIL_HOST_USER,
                    recipients, fail_silently=False)

    def handle(self, *args, **options):
        self.get_status()

