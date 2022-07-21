from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from jazda.models import Przystanek, Godzina, Rozklad
from jazda.views.rozklad import godz_odj_rozklad, przystankiSzczecinek, odjazdyMeta, godziny_jazdy
from jazda.views.rozklady import rozklad_www
from django.shortcuts import render
from calendar import HTMLCalendar
from datetime import date


def lista_przystankow(powrot=0):
    slownik = {}
    order_by = ['id', 'godzina']
    #  kierunek = ['odjazdy w kierunku m. Czarne', 'odjazdy w kierunku Szczecinka']
    przystanki = Przystanek.objects.filter(godzina__in=godz_odj_rozklad(powrot)).order_by(order_by[powrot])

    for item_p in przystanki:
        for item_g in godz_odj_rozklad(powrot):
            if item_p.id == item_g.przystanek_id:
                slownik[item_p.nazwa] = {
                    'id': item_p.id,
                    'opis': item_p.opis,
                    'opis_2': item_p.opis_drugi
                }

    return slownik


def przystanki(request):

    return render(request, 'jazda/przystanki2.html', {
        'kierunek_tam': 'ODJAZDY',
        'kierunek_powrot': 'POWROTY',
       # 'przystanki_tam': lista_przystankow(),
        #'przystanki_powrot': lista_przystankow(1),
       # 'slownik': rozklad_www()

    }
    )