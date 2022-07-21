from django.shortcuts import render
from django.http import  HttpResponseRedirect
from datetime import datetime, date
import calendar
from calendar import HTMLCalendar
from events.models import Event, Venue
from events.forms import VenueForm
from jazda.models import Rozklad, Przystanek, Godzina
from django.core import serializers
from django.template.response import TemplateResponse


# Create your views here.
def index(request, year=date.today().year, month=date.today().month):
    # t = date.today()
    # usr = request.user
    # ses = request.session
    # path = request.path
    # path_info = request.path_info
    # headers = request.headers
    # assert False
    month = int(month)
    year = int(year)
    if year < 2000 or year > 2099: year = date.today().year
    month_name = calendar.month_name[month]
    title = "MyClub Event Calendar - %s %s" %(month_name, year)
    cal = HTMLCalendar().formatmonth(year, month)
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
    #return HttpResponse(f"<h1>{title}</h1><p>{cal}</p>")
    # to poniżej też działa tak samo
    #return HttpResponse("<h1>%s</h1>" % title)
    return TemplateResponse(request, 'events/calendar_base.html', {'title': title, 'cal': cal, 'announcements': announcements})

# def rozklad(request):
#     # rozklad_list = Rozklad.objects.all()
#     przystanki = Przystanki.objects.all()
#     godziny = Godzina.objects.all()
#     return  render(request, 'events/rozklad.html', {'przystanki': przystanki, 'godziny': godziny})

def all_events(request):
    event_list = Event.objects.all()
    return render(request, 'events/event_list.html', {'event_list': event_list})

def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_venue/?submitted=True')
    else:
        form = VenueForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def template_demo(request):
    empty_list = []
    color_list = ['red', 'green', 'blue', 'yellow', 'black']
    somevar = 5
    anothervar = 21
    today = datetime.now()
    past = datetime(1985, 11, 5)
    future = datetime(2035, 11, 5)
    best_bands = [
        {'name': 'The Angels', 'country': 'Australia'},
        {'name': 'AC/DC', 'country': 'Australia'},
        {'name': 'Nirvana', 'country': 'USA'},
        {'name': 'The Offspring', 'country': 'USA'},
        {'name': 'Iron Maiden', 'country': 'UK'},
        {'name': 'Rammstein', 'country': 'Germany'},
    ]
    aussie_bands = ['Australia', ['The Angels', 'AC/DC', 'The Living End']]
    venues_js = serializers.serialize('json', Venue.venues.all())
    return render(request,
        'events/template_demo.html',
        {
            'somevar': somevar,
            'anothervar': anothervar,
            'empty_list': empty_list,
            'color_list': color_list,
            'best_bands': best_bands,
            'today': today,
            'past': past,
            'future': future,
            'aussie_bands': aussie_bands,
            'venues': venues_js,
        }
    )
