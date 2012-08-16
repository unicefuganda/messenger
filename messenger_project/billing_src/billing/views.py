from django.conf import settings
from django.utils.datastructures import SortedDict
from django.db.models import Count
from rapidsms.models import Backend
from rapidsms_httprouter.models import Message
import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext

PROJECT_BACKENDS = {
    'dmark':['ureport', 'mtrack'],
    'yo6200':['edtrac'],
    'yo8200':['mtrack'],
    'utl':['ureport', 'mtrack', 'edtrac'],
    'zain':['ureport', 'mtrack', 'edtrac'],               
    }
    
PROJECTS = ["ureport", "edutrac", "mtrack"]

NETWORK_PREFIXES = (
    ('mtn', '25677'),
    ('warid', '25670'),
    ('airtel', '25675'),
    ('orange', '25679'),
    ('utl', '25671'),
) 

def network_traffic(request, **kwargs):
    directions = {'I':'Incoming', 'O':'Outgoing'}
    messages = SortedDict()
    d = datetime.datetime.now()
    years = range(2012, d.year + 1)
    start_date = datetime.datetime(2012, 1, 1)
    months = range(1, d.month+1)
    # proj = kwargs.get('proj')

    for y in years:
        messages[y] = SortedDict()
        for m in months:
            messages[y][m] = SortedDict()
            for d, direction in directions.items():
                messages[y][m][d] = SortedDict()
                for n, p in NETWORK_PREFIXES:
                    messages[y][m][d][n] = 0
    
    for d, direction in directions.items():
        for network_name, prefix in NETWORK_PREFIXES:
            app_messages = Message.objects.using(kwargs.get('project'))\
                    .filter(date__gte=start_date)\
                    .filter(direction=d)\
                    .filter(connection__identity__startswith=prefix)\
                    .exclude(status__in=['L', 'P', 'Q', 'C'])\
                    .extra({'year':'extract (year from rapidsms_httprouter_message.date)', \
                             'month':'extract (month from rapidsms_httprouter_message.date)'})\
                    .values('year', 'month', 'direction')\
                    .annotate(total=Count('id'))\
                    .extra(order_by=['year', 'month', 'direction'])
            for dct in app_messages:
                y = int(dct['year'])
                m = int(dct['month'])
                d = dct['direction']
                n = network_name
                t = dct['total']
                messages[y][m][d][n] += t
                      
    return render_to_response(
        "billing/network_traffic.html",
        {
         'years':years,
         'months':months,
         'directions':directions,
         'messages':messages,
         'networks': NETWORK_PREFIXES,
         'projects': PROJECTS,
         }, context_instance=RequestContext(request))


def summary(request):
    messages = SortedDict()
    prjs = SortedDict()
    d = datetime.datetime.now()
    years = range(2010, d.year + 1)
    start_date = datetime.datetime(2010, 1, 1)
    months = range(1, 13)
    backends = []
    dbs = settings.DATABASES.keys()
    for db in dbs:
        if db == 'default':
            continue
        bs = list(Backend.objects.using(db).exclude(name='console').exclude(name='TestBackend').exclude(connection__backend__name__icontains='modem').order_by('name').values_list('name', flat=True))
        for b in bs:
            if b not in backends:
                backends.append(b)
    backends = sorted(backends)

    directions = ['I', 'O']
    for y in years:
        messages[y] = SortedDict()
        for m in months:
            messages[y][m] = SortedDict()
            for b in backends:
                messages[y][m][b] = SortedDict()
                for d in directions:
                    messages[y][m][b][d] = 0

    for db in dbs:
        if db == 'default':
            continue
        app_messages = Message.objects.using(db)\
                .filter(date__gte=start_date)\
                .exclude(status__in=['L', 'P', 'Q', 'C'])\
                .exclude(connection__backend__name='console')\
                .exclude(connection__backend__name='console').exclude(connection__backend__name='TestBackend').exclude(connection__backend__name__icontains='modem')\
                .extra({'year':'extract (year from rapidsms_httprouter_message.date)', \
                         'month':'extract (month from rapidsms_httprouter_message.date)'})\
                .values('year', 'month', 'connection__backend__name', 'direction')\
                .annotate(total=Count('id'))\
                .extra(order_by=['year', 'month', 'connection__backend__name', 'direction'])
        for dct in app_messages:
            y = int(dct['year'])
            m = int(dct['month'])
            b = dct['connection__backend__name']
            d = dct['direction']
            t = dct['total']
#            prjs[db] = t
            messages[y][m][b][d] += t 
            
    dbs.remove('default')
    return render_to_response(
        "billing/summary.html",
        { 'messages':messages, 
         'backends':backends, 
         'db_count':len(dbs),
         'pbackends': PROJECT_BACKENDS,
         }, context_instance=RequestContext(request))
    
def utl_summary(request):
    messages = SortedDict()
    prjs = SortedDict()
    d = datetime.datetime.now()
    years = range(2010, d.year + 1)
    start_date = datetime.datetime(2010, 1, 1)
    months = range(1, 13)
    backends = []
    dbs = settings.DATABASES.keys()
    for db in dbs:
        if db == 'default':
            continue
        bs = list(Backend.objects.using(db).filter(name='utl').values_list('name', flat=True))
        for b in bs:
            if b not in backends:
                backends.append(b)
    backends = sorted(backends)

    directions = ['I', 'O']
    for y in years:
        messages[y] = SortedDict()
        for m in months:
            messages[y][m] = SortedDict()
            for b in backends:
                messages[y][m][b] = SortedDict()
            for d in directions:
                messages[y][m][b][d] = 0

    for db in dbs:
        if db == 'default':
            continue
        app_messages = Message.objects.using(db)\
                .filter(date__gte=start_date)\
                .exclude(status__in=['L', 'P', 'Q', 'C'])\
                .filter(connection__identity__startswith='25671')\
                .exclude(connection__backend__name__startswith='yo')\
                .extra({'year':'extract (year from rapidsms_httprouter_message.date)', \
                         'month':'extract (month from rapidsms_httprouter_message.date)'})\
                .values('year', 'month', 'connection__backend__name', 'direction')\
                .annotate(total=Count('id'))\
                .extra(order_by=['year', 'month', 'connection__backend__name', 'direction'])
        
        for dct in app_messages:
            y = int(dct['year'])
            m = int(dct['month'])
            b = u'utl'
            d = dct['direction']
            t = dct['total']
#            prjs[db] = t
            messages[y][m][b][d] += t 
    print messages        
    dbs.remove('default')
    return render_to_response(
        "billing/utl_summary.html",
        { 'messages':messages, 
         'backends':backends, 
         'db_count':len(dbs),
         'pbackends': PROJECT_BACKENDS,
         }, context_instance=RequestContext(request))
    
def detail(request, **kwargs):
    directions = {'I':'Incoming', 'O':'Outgoing'}
    messages = SortedDict()
    d = datetime.datetime.now()
    years = range(2010, d.year + 1)
    start_date = datetime.datetime(2010, 1, 1)
    months = range(1, 13)
    backend = kwargs.get('backend')

    for y in years:
        messages[y] = SortedDict()
        for m in months:
            messages[y][m] = SortedDict()
            for d, direction in directions.items():
                messages[y][m][d] = 0
    
    for d, direction in directions.items():
        app_messages = Message.objects.using(kwargs.get('project'))\
                    .filter(date__gte=start_date)\
                    .filter(direction=d)\
                    .filter(connection__backend__name=backend)\
                    .exclude(status__in=['L', 'P', 'Q', 'C'])\
                    .extra({'year':'extract (year from rapidsms_httprouter_message.date)', \
                             'month':'extract (month from rapidsms_httprouter_message.date)'})\
                    .values('year', 'month', 'direction')\
                    .annotate(total=Count('id'))\
                    .extra(order_by=['year', 'month', 'direction'])
        for dct in app_messages:
            y = int(dct['year'])
            m = int(dct['month'])
            d = dct['direction']
            t = dct['total']
            messages[y][m][d] += t
                      
    return render_to_response(
        "billing/detail.html",
        {
         'years':years,
         'months':months,
         'directions':directions,
         'messages':messages,
         'pbackends': PROJECT_BACKENDS,
         }, context_instance=RequestContext(request))

