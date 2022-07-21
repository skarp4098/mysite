from django.shortcuts import render
from django.http import  HttpResponseRedirect
from datetime import date
import calendar
from calendar import HTMLCalendar
from .models import Event
from .forms import VenueForm
from jazda.models import Rozklad, Przystanek, Godzina


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
    return render(request, 'events/calendar_base.html', {'title': title, 'cal': cal, 'announcements': announcements})

# def rozklad(request):
#     # rozklad_list = Rozklad.objects.all()
#     przystanki = Przystanki.objects.all()
#     godziny = Godzina.objects.values_list()
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



