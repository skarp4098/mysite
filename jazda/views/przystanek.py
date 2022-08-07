# import ast
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from jazda.models import Przystanek, Godzina, Rozklad, Miasto
from jazda.views.rozklady import etykiety_godzin_th  #  , przystanek_odjazdy
from django.shortcuts import render
from calendar import HTMLCalendar
from datetime import date


# def flatten_out_nested_list(input_list):
#     if input_list is None:
#         return None
#     if not isinstance(input_list, (list, tuple)):
#         return None
#     flattened_list = []
#     for entry in input_list:
#         entry_list = None
#         if not isinstance(entry, list):
#             try:
#                 entry_list = ast.literal_eval(entry)
#             except:
#                 pass
#         if not entry_list:
#             entry_list = entry
#         if isinstance(entry_list, list):
#             flattened_entry = flatten_out_nested_list(entry_list)
#             if flattened_entry:
#                 flattened_list.extend(flattened_entry)
#         else:
#             flattened_list.append(entry)
#     return flattened_list

# def przystanek_odjazdy(przyst_id, powrot=0):
#     """Funkcja tworzy słownik opisujący przystanek także jeśli obowiązuje więcej niż jednen
#     rozkład jazdy"""
#
#     slownik = {}
#     # w przypadku wielu obowiązujących rozkładów pełne godziny odjazdów w postaci wielu list
#     lista_list = []
#
#     etykiety_godzin = []
#     # tymczasowy słownik informacji dla konkretnego przystanku
#     slownik_temp = rozklad_dla_www(powrot, przyst_id)
#
#     for item in slownik_temp.values():
#         temp_value = str(item['etykiety_godzin'])
#         lista_list.append(temp_value)
#
#     # spłaszczam tablice do jednej ze wszystkimi wartościami
#     jedna_lista = flatten_out_nested_list(lista_list)
#
#     # eliminuje duplikaty godzin
#     for item in jedna_lista:
#         if item not in etykiety_godzin:
#             etykiety_godzin.append(item)
#
#
#     for key, value in slownik_temp.items():
#             slownik[key] = {
#                 'kierunek': value['kierunek'],
#                 'od': value['od'],
#                 'opis':  value['opis_rozkladu'],
#                 'etykiety': etykiety_godzin,
#                 'przystanek': value['przystanek'],
#
#             }
#     return slownik

def przystanek_info(przyst_id, odjazdy):
    slownik2 = {}

    przystanek_db = Przystanek.objects.filter(id=przyst_id)
    for item in przystanek_db:
        slownik2[item.nazwa] = {
            'id': item.id,
            'opis': item.opis,
            'opis2': item.opis_drugi,
            'dlugosc': item.dlugosc,
            'szerokosc': item.szerokosc,
            # dodaje slownik z godzinami odjazdów
            'godzina': odjazdy
        }
    return slownik2


def godziny_dni_powszednie(przyst_id, rozkl_id, powrot, godzina):
    odjazdy = []
    jeden_odjazd = ''
    godziny_powszednie = Godzina.objects.filter(przystanek_id=przyst_id, rozklad_id=rozkl_id,
                                        powrot=powrot, godzina__startswith=str(godzina)[0:2])

    for item in godziny_powszednie:
        if not item.sobota and item.zjazd_do_skotnik:
            odjazdy.append(str(item)[3:5] + "'z ")
            jeden_odjazd = str(item)[3:5] + "'z "
        elif not item.sobota:
            odjazdy.append(str(item)[3:5] + "' ")
            jeden_odjazd = str(item)[3:5] + "' "

    if len(odjazdy) > 1:
        return odjazdy
    else:
        return jeden_odjazd


def godziny_sobota(przyst_id, rozkl_id, powrot, godzina):
    """Funkcja ustala godziny odjazdów w dni powszednie dla strony przystanek.html"""
    odjazdy_sobota = []
    godz_sobota = Godzina.objects.filter(przystanek_id=przyst_id, rozklad_id=rozkl_id, sobota=1,
                                    powrot=powrot, godzina__startswith=str(godzina)[0:2])
    jeden_odjazd = ''

    for item in godz_sobota:
        if item.zjazd_do_skotnik and item.sobota:
            odjazdy_sobota.append(str(item)[3:5] + "'sz ")
            jeden_odjazd = str(item)[3:5] + "zs"
        elif item.sobota:
            odjazdy_sobota.append(str(item)[3:5] + "'s ")
            jeden_odjazd = str(item)[3:5] + "'s "

    if len(odjazdy_sobota) > 1:
        return odjazdy_sobota
    else:
        return jeden_odjazd


def przystanek_odjazdy(przyst_id, rozkl_id, powrot):
    """Funkcja ustala godziny odjazdów dla przystanku"""
    slownik = {}
    odjazdy_powszednie = []
    object = Godzina.objects.filter(przystanek_id=przyst_id, rozklad_id=rozkl_id, powrot=powrot) #, godzina__startswith=str(godzina)[0:2])
    jeden_odjazd = ''

    for item_g in object:
        if item_g.przystanek_id == przyst_id:
            slownik[str(item_g)[0:2]] = {
                'daily': godziny_dni_powszednie(przyst_id, rozkl_id, powrot, item_g.godzina),
                'sobota': godziny_sobota(przyst_id, rozkl_id, powrot, item_g.godzina)
            }

    return slownik


def miasto(przyst_id):
    miasto_www = ''
    id_miasta = 0
    przystanek_miasto = Przystanek.objects.filter(id=przyst_id)
    for item in przystanek_miasto:
        id_miasta = item.miasto_id

    miasto = Miasto.objects.filter(id=id_miasta)
    for item in miasto:
        miasto_www = item.nazwa
    return miasto_www


def rozklad_dla_przystanku(powrot, przyst_id):
    """Funkcja dla strony przystanek.html"""
    slownik = {}

    # obowiazujace rozklady
    rozklad_items = Rozklad.objects.filter(na_stronie__exact=1)

    # godziny dla rozkładu/rozkładów
    # godzina_items = Godzina.objects.filter(rozklad_id__in=rozklad_items, powrot=powrot, przystanek_id=przyst_id)

    for item_r in rozklad_items:
        etykiety = etykiety_godzin_th(item_r.id, powrot, przyst_id)
        odjazdy = przystanek_odjazdy(przyst_id, item_r.id, powrot)
        # for item_g in godzina_items:
        # for __ in range(len(godzina_items)):
        # if przyst_id == item_g.przystanek_id:
        slownik[item_r.nazwa] = {
            'od': str(item_r.od),
            'do': str(item_r.do),
            'desc': item_r.description,
            'etykiety_godzin': etykiety,
            'przystanek': przystanek_info(przyst_id, odjazdy),
        }
    return slownik


def przystanek(request, value_id, powrot=0): # value_id to przystanek_id

    ety_kier = ['Gwda >> Czarne', 'Gwda >> Szczecinek']
    kierunek = ety_kier[powrot]
    if value_id == 1:
        kierunek = ' Szczecinek >> Gwda >> Czarne'
    spot = get_object_or_404(Przystanek, id=value_id)

   # ulica = False bylo if ulica na stronie
    zjazd = True
    if powrot == 0:
        zjazd = False

    if str(spot).startswith("ul."):
        temp = str(spot).lstrip(", ul.")
        x = temp.find(",")
        etykieta_th = temp[0:x]
        #x = etykieta_th.find(" ")
        #etykieta_th = etykieta_th[0:x]
     #   ulica = True
    else:
        x = str(spot).find(",")
        etykieta_th = str(spot)[0:x]

    return render(request, 'jazda/przystanek.html', {
                                                     'spot': spot,
                                                     'dlugosc': spot.dlugosc,
                                                     'szerokosc': spot.szerokosc,
                                                     'etykieta_th': etykieta_th.lower(),
                                                     'zjazd': zjazd,
                                                     'kierunek': kierunek,
                                                     'miasto': miasto(value_id),
                                                     'przystanek':  rozklad_dla_przystanku(powrot, value_id),
                                                   # 'data': data,
                                                     })