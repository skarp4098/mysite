from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from jazda.models import Przystanek, Godzina, Rozklad
from jazda.views.rozklad import godz_odj_rozklad, odjazdyMeta, godziny_jazdy
from django.shortcuts import render
from calendar import HTMLCalendar
from datetime import date


def rozklady_na_stronie():
    """Funkcja tworzy objekt rozkladu/ów wskazanych przez admina do wyświetlenia w internecie"""

    object_db_rozklad = Rozklad.objects.filter(na_stronie__exact=1)

    return object_db_rozklad


def przystanki_do_tabeli(id, powrot=0):

    wynik = Godzina.objects.filter(rozklad_id=id, powrot=powrot)  #.order_by('przystanek_id')
    if powrot == 0:
        przystanki = Przystanek.objects.filter(godzina__in=wynik).order_by('id', 'godzina')
    else:
        przystanki = Przystanek.objects.filter(godzina__in=wynik).order_by('godzina', 'id')

    return przystanki


def przystanek_sobota(godzina_items, przyst_id, godzina):
    """Funkcja ustala sobotnie godziny odjazdów dla strony przystanek.html"""
    odjazdy_sobota = []
    object = godzina_items.filter(przystanek_id=przyst_id, godzina__startswith=str(godzina)[0:2])
    jeden_odjazd = ''

    for item in object:
        if item.zjazd_do_skotnik and item.sobota:
            odjazdy_sobota.append(str(item)[0:5] + "zs")
            jeden_odjazd = str(item)[0:5] + "zs"
        elif item.sobota:
            odjazdy_sobota.append(str(item)[0:5] + " s")
            jeden_odjazd = str(item)[0:5] + " s"


    if len(odjazdy_sobota) > 1:
        return odjazdy_sobota
    else:
        return jeden_odjazd

def przystanek_dzien_powszedni(godzina_items, przyst_id, godzina):
    """Funkcja ustala godziny odjazdów w dni powszednie dla strony przystanek.html"""
    odjazdy_powszednie = []
    object = godzina_items.filter(przystanek_id=przyst_id, godzina__startswith=str(godzina)[0:2])
    jeden_odjazd = ''

    for item in object:
        if not item.sobota:
            odjazdy_powszednie.append(str(item)[0:5])
            jeden_odjazd = str(item)[0:5]

    if len(odjazdy_powszednie) > 1:
        return odjazdy_powszednie
    else:
        return jeden_odjazd

def helper(godzina_items, przyst_id, godzina):
    """Funkcja ustala godziny odjazdów w zbiorczym rozkładzie jazdy"""

    odjazdy = []
    jeden_odjazd = ''

    object = godzina_items.filter(przystanek_id=przyst_id, godzina__startswith=str(godzina)[0:2])  # .order_by('przystanek_id')

    for item in object:
        if item.sobota and item.zjazd_do_skotnik:
            odjazdy.append(str(item)[0:5] + " sz")
            jeden_odjazd = str(item)[0:5] + " sz"
        elif item.zjazd_do_skotnik:
            odjazdy.append(str(item)[0:5] + "z")
            jeden_odjazd = str(item)[0:5] + "z"
        elif item.sobota:
            odjazdy.append(str(item)[0:5] + " s")
            jeden_odjazd = str(item)[0:5] + " s"
        else:
            odjazdy.append(str(item)[0:5]) # + ", ")
            jeden_odjazd = str(item)[0:5] #  + " ' "

    if len(odjazdy) > 1:
        return odjazdy
    else:
        return jeden_odjazd

def ustal_godzine(godzina_items, przyst_id, flaga):
# def ustal_godzine(rozklad_id, powrot, przyst_id, flaga):
    # rozkład zbiorczy
    slownik3 = {}

#    godzina_items = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot,
                                          # przystanek_id=przyst_id)  # .order_by('przystanek_id')

    for godzina in godzina_items:
        polecenie = helper(godzina_items, przyst_id, godzina)
        if flaga == 1:
            polecenie = przystanek_dzien_powszedni(godzina_items, przyst_id, godzina)
        slownik3[str(godzina)[0:2]] = {
          # 'min': helper(godzina_items, przyst_id, godzina),
           'min': polecenie,
           'sobota': przystanek_sobota(godzina_items, przyst_id, godzina),
            }
    return slownik3


def godziny_odjazdow_dla_przystanku(rozklad_id, powrot=0, przyst_id=0):
    """Funkcja ustala godziny odjazdów dla aktywnych rozkladów"""
    slownik2 = {}
    # dla strony przystanek.html jeśli kod przypisze 1 zmiennej flaga
    flaga = 0

    # dla jednego przystanku
    if przyst_id > 0:
        flaga = 1
        godzina_items = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot,
                                               przystanek_id=przyst_id)  # .order_by('przystanek_id')

    # dla wszystkich przystanków
    else:
        godzina_items = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot)#.order_by('przystanek_id')

    for item_p in przystanki_do_tabeli(rozklad_id, powrot):
        for item_g in godzina_items:
            if item_p.id == item_g.przystanek_id:
                slownik2[item_p.nazwa] = {
                    'id': item_p.id,
                    'opis': item_p.opis,
                    'opis2': item_p.opis_drugi,
                    'godzina': ustal_godzine(godzina_items, item_g.przystanek_id, flaga),
                   # 'godzina': ustal_godzine(rozklad_id, powrot, item_g.przystanek_id, flaga),
                }

    return slownik2

def etykiety_godzin_th(rozklad_id, powrot=0, przyst_id=0):
    """Funkcja przygotowuje etykiety pełnych godzin dla poszczególnych kolumn <th> rozkładu jazdy"""
    etykieta_godziny = []
    # dla przystanku
    if przyst_id > 0:
        godziny = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot, przystanek_id=przyst_id).order_by('godzina')
    # dla wszystkich przystanków
    else:
        godziny = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot).order_by('godzina')

    for item in godziny:
        # przycięta do pełnej, godzina z DB
        temp_godz = str(item.godzina)[0:2]
        # zapisuje tylko jedno wystąpienie pełnej godziny
        if temp_godz not in etykieta_godziny:
            etykieta_godziny.append(temp_godz)

    return etykieta_godziny


def rozklad_dla_www(powrot=0, przyst_id=0):
    slownik1 = {}
    ety_kier = ['odjazdy w kierunku m. Czarne', 'odjazdy w kierunku Szczecinka']

    # dla konkretnego przystanku
    if przyst_id > 0:
        for item in rozklady_na_stronie():
            slownik1[item.nazwa] = {
              'kierunek': ety_kier[powrot],
              'id': item.id,
              'od': str(item.od),
              'do': str(item.do),
              'desc': item.description,
              'etykiety_godzin': etykiety_godzin_th(item.id, powrot, przyst_id),
              'przystanek': godziny_odjazdow_dla_przystanku(item.id, powrot, przyst_id),
                }

        # sposób na odczytywanie wartości słownika w pliku .py
        # for key, value in rozklady_na_stronie().items():
        #     slownik1[key] = {
        #         'kierunek': ety_kier[powrot],
        #         'od': value['od'],
        #         'opis_rozkladu': value['desc'],
        #         'etykiety_godzin': etykiety_godzin_th(value['id'], powrot, przyst_id),
        #         'przystanek': godziny_odjazdow_dla_przystanku(value['id'], powrot, przyst_id)
        #     }

    # dla wszystkich przystanków
    else:
        for item in rozklady_na_stronie():
            slownik1[item.nazwa] = {
                'kierunek': ety_kier[powrot],
                'id': item.id,
                'od': str(item.od),
                'do': str(item.do),
                'desc': item.description,
                'etykiety_godzin': etykiety_godzin_th(item.id, powrot),
                'przystanek': godziny_odjazdow_dla_przystanku(item.id, powrot),
            }
    return slownik1

def proby(request):

    return render(request, 'jazda/proby.html',{
       # 'cont': rozklady_na_stronie(),
       # 'dict': dict,
        'rozklad_tam': rozklad_dla_www(),
        'rozklad_powrot': rozklad_dla_www(1),

    }
    )