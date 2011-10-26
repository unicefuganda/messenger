from django.conf import settings

def summary(req):
    for db in settings.DATABASES.keys():
        messages = Message.objects.using(db).extra(
                       {'year':'extract(year from date)',
                        'month':'extract (month from date)'})\
                   .values('year', 'month', 'connection__backend__name', 'direction')\
                   .annotate(total=Count('id'))\
                   .extra(order_by=['year', 'month', 'connection__backend__name', 'direction'])
    return render_to_response(
        "router/summary.html",
        { 'messages': messages}, context_instance=RequestContext(request))


# 'connection__backend__name'
# 'total'
# direction
# year
# month
