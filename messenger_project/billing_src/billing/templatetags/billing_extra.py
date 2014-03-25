from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]

@register.filter
def add_to_list(input, property):
    if type(input) == list:
        return input + [property]
    else:
        return [property]
    
@register.filter
def extract_value(input, property):
    return input[property[0]][property[1]][property[2]]
    
@register.filter
def extract_values(input, property):
    values = input[property[0]][property[1]][property[2]]
    toret = ''
    str_list = []
    for n, v in values.items():
        str_list.append('%s:%d' % (n, v))
    return '\n'.join(str_list)

@register.filter
def make_k(value):
    return value/1000