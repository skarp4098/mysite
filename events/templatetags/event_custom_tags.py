from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime

register = template.Library()

@register.filter(name='reverse')
@stringfilter
def reverse(value):
    return value[::-1]

@register.simple_tag
def create_date(date_val):
    return "This content was created on %s" %date_val.strftime('%A %B %d %Y')

@register.inclusion_tag('events/announcements.html')
def announcements():
    announcements = [
        {
            'date': '10-10-2022',
            'announcement': "Club Registrations Open"
        },
        {
            'date': '15-10-2022',
            'announcement': "Joe Smith Elected New Club President"
        }
    ]
    return {'announcements': announcements}
