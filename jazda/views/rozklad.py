from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
#from  django.template.loader import render_to_string
from  django.urls import reverse
from jazda.models import Przystanek, Godzina, Rozklad
from  django.shortcuts import render
from django.views.generic import ListView
from django.core import serializers
from django.utils.timezone import datetime

# Create your views here.

content = {

    'rozklad': "Tu bedzie rozkladddd",
    'oferta': 'Tu bedzie oferta',
    'bilety': 'Tu bedzie o biletach'
}


class OdjazdyListView(ListView):
    model = Przystanek


# def drive_challenge(request, desire):
#     try:
#         odp = content[desire]
#         # dla template
#         return render(request, 'jazda/jazda.html', {
#             'text': odp,
#         })
#         # dla template inaczej
#         #odp = render_to_string('jazda/jazda.html')
#     except:
#         return HttpResponseNotFound('Taki content nie istnieje 404')
#     #return  HttpResponse(odp)

def index(request):
    menu_items = ''
    menu = list(content.keys())

    return render(request, 'jazda/index.html', {

        'menu': menu
    })
    # for item in menu:
    #     z_duzej_item = item.capitalize()
    #     redirect_path = reverse('drive-challenge', args=[item])
    #     menu_items += f'<li><a href=\'{redirect_path}\'>{z_duzej_item}</a></li>'
    #
    # response_data = f'<ul>{menu_items}</ul>'
    # return HttpResponse(response_data)


def godziny_jazdy(czy_powrot=0):
    """Funkcja przygotowuje etykiety pełnych godzin dla poszczególnych kolumn <th> rozkładu jazdy"""

    etykieta_godziny = []
    if czy_powrot > 1:
        godziny = Godzina.objects.all().order_by('godzina')
    else:
        godziny = godz_odj_rozklad(czy_powrot)
    for item in godziny:
        # godzina do tabeli rozklad
        temp_godz = str(item.godzina)[0:2]
        # zapisuje tylko jedno wystąpienie pełnej godziny
        if not temp_godz in etykieta_godziny:
            etykieta_godziny.append(temp_godz)
    return  etykieta_godziny

def odjazdy(id_przyst, godzina):
    """Funkcja generuje godziny odjazdów dla rozkladu, także w przypadku gdy w trakcie jednej godziny
    z tego samego przystanku w tym samym kierunku odjeżda kilka kursóœ"""
    odjazdy = []
    jeden_odjazd = ''

    id_r = Rozklad.objects.filter(na_stronie__exact=1)
    hours = Godzina.objects.filter(przystanek_id=id_przyst, rozklad_id__in=id_r,
                                   godzina__startswith=str(godzina)[0:2]).order_by('godzina')

    for item in hours:
        if item.zjazd_do_skotnik:
            odjazdy.append(str(item)[0:5] + "*")
            jeden_odjazd = str(item)[0:5] + "*"
        elif item.godziny_sobota:
            odjazdy.append(str(item)[0:5] + " s")
            jeden_odjazd = str(item)[0:5] + " s"
        else:
            odjazdy.append(str(item)[0:5]) # + " ' ")
            jeden_odjazd = str(item)[0:5]  # + " ' "
    if len(odjazdy) > 1:
        return odjazdy
    else:
        return jeden_odjazd



def odjazdyMeta(id_przyst, czy_powrot=0):
    """Funkcja tworzy słownik pełnych godzin odjazdów(key) i minut (value)"""
    dict = {}
    godziny = godziny_jazdy(czy_powrot) # lista pełnych godzin w nagłówku th rozkładu uszczuplona do jednego wystąpienia

    # poniżej kupa
    # godziny = godz_odj_rozklad(czy_powrot)

    for godzina in godziny:
        dict[godzina] = {
           'min': odjazdy(id_przyst, godzina)
            }

    # for godzina in godziny:
    #      for odjazd in lista_odjazdow:
    #         # jeśli godzina odjazdu pasuje do tej z nagłówka th rozkladu umieszcza ją w tej kolumnie
    #         if odjazd.startswith(godzina):
    #             #lista_do_rozkladu.insert(i, odjazdy(id_przyst, godzina))
    #             lista_do_rozkladu.insert(i, odjazd)
    #         elif not odjazd.startswith(godzina):
    #             lista_do_rozkladu.append('')
    #      i += 1
    # # procedura usuwa nieporzebne puste komórki, które tworzą się podczas generowania rozkładu
    # if len(lista_do_rozkladu) > len(godziny):
    #    for i in range(len(lista_do_rozkladu)):
    #        if i >= len(godziny):
    #            lista_do_rozkladu.pop()


    # for odjazd in lista:
    #     if odjazd.startswith('05'):
    #         nowa_lista.append(odjazd)
    #     else:
    #         nowa_lista.append('5')
    #     if odjazd.startswith('06'):
    #         nowa_lista.insert(1, odjazd)
    #     else:
    #         nowa_lista.append('6')
    #     if odjazd.startswith('07'):
    #         nowa_lista.insert(2, odjazd)
    #     else:
    #         nowa_lista.append('')
    #     if odjazd.startswith('08'):
    #         nowa_lista.insert(3, odjazd)
    #     else:
    #         nowa_lista.append('')
    #     if odjazd.startswith('09'):
    #         nowa_lista.insert(4, odjazd)
    #     else:
    #         nowa_lista.append('')

       # elif not odjazd.startswith('05'):


    #nowa_lista = lista_odjazdow

    return dict  # dict

def rozklad_id_DB():
    conteiner_id_rozklad = []
    id_rozklad = Rozklad.objects.filter(na_stronie__exact=1)

    for id in id_rozklad:
        conteiner_id_rozklad.append(str(id))

    return conteiner_id_rozklad


def rozkladDB():
    """Funkcja ustala rozklad jazdy oznaczony jako aktualny dla www"""
    conteiner_id_rozklad = []
    id_rozklad = Rozklad.objects.filter(na_stronie__exact=1)

    for id in id_rozklad:
        conteiner_id_rozklad.append(str(id))

    return id_rozklad

def przystankiWszystkie():
    """Funkcja zwraca listę wszystkich przystanków będących w DB"""

    # id_g = Godzina.objects.raw('Select godzina_id form jazda_godzina_rozklad where rozklad_id = 1')
    wszystkie = Przystanek.objects.all()
    return wszystkie

def przystankiSzczecinek():
    """Funkcja zwraca listę przystanków w Szczecinku plus Skotniki, Gwda kier. Czarne"""

    przystankiSzek = Przystanek.objects.filter(godzina__in=godz_odj_rozklad(0)).order_by('godzina')

    return przystankiSzek


def przystankiPowrotne():
    """Funkcja zwraca listę przystanków powrotnych: Czarne, Gwda, Szczecinek w kierunku Skotnik"""

    przystankiPowrot = Przystanek.objects.filter(godzina__in=godz_odj_rozklad(1)).order_by('godzina')

    return przystankiPowrot


def godz_odj_rozklad(czy_powrot=0):

    #id_r = Rozklad.objects.get(na_stronie__exact=1)
    # dla wszystkich godzin: wyjazd i powrót razem
    if czy_powrot > 1:
        obj_query = Godzina.objects.filter(przystanek_id__in=przystankiWszystkie(), rozklad_id__in=rozkladDB())
    # określone parametrem 'czy_powrot': dla zera godziny wyjazdów, dla 1 godziny powrotów
    else:
        obj_query = Godzina.objects.filter(przystanek_id__in=przystankiWszystkie(),
                                           powrot__contains=czy_powrot, rozklad_id__in=rozkladDB())

    return obj_query


def rozklad_szek():
    roz_szek = {}
    czy_powrot = 0

    for item_p in przystankiSzczecinek():
        sobota = []
        powrot = []
        for item_g in godz_odj_rozklad(0):
            if item_p.id == item_g.przystanek_id:
                sobota.append(item_g.godziny_sobota)
                powrot.append(item_g.powrot)
                roz_szek[item_p.nazwa] = {
                    'id': item_p.id,
                    'opis': item_p.opis,
                    'odjazd': {
                        'godzina': odjazdyMeta(item_g.przystanek_id, czy_powrot),
                        'sobota': sobota,
                        'powrot': powrot,
                    }
                }

    return roz_szek

def rozklad_powrot():
    roz_powrot = {}
    czy_powrot = 1

    for item_p in przystankiPowrotne():
        godz = []
        sobota = []
        powrot = []
        # parameter 1 w godz_odj_rozklad oznacza przystanki-godziny powrotne
        for item_g in godz_odj_rozklad(1):
            if item_p.id == item_g.przystanek_id:
                godz.append(str(item_g.godzina)[0:5])
                sobota.append(item_g.godziny_sobota)
                powrot.append(item_g.powrot)
                roz_powrot[item_p.nazwa] = {
                    'id': item_p.id,
                    'opis': item_p.opis,
                    'odjazd': {
                        'godzina': odjazdyMeta(item_g.przystanek_id, czy_powrot),
                        'sobota': sobota,
                        'powrot': powrot,

                    }

                }

    return roz_powrot

def rozklad(request):
    rozklad = {}
    czy_powrot = 2
    # poniżej filtruje id przystanku dla którego występuje godzina odjazdu przypisana do rozkladu jazdy
    # g = Godzina.objects.filter(rozklad__na_stronie__exact=1)

    #wszystkie = Przystanek.objects.filter(id__contains=g)
    godziny = Godzina.objects.all().order_by('godzina')
    godziny_od_do = Godzina.objects.values('godzina').order_by('godzina')
    godziny_lists = Godzina.objects.values_list('godzina').order_by('godzina')

    #przyst = Przystanki.objects.all()
    # obj = Godzina.objects.filter(przystanek_id__in=przyst, powrot__contains=0)
    obj = Godzina.objects.filter(przystanek_id__in=przystankiWszystkie())
    # obj = Godzina.objects.filter(przystanek_id__in=przyst).order_by('godzina')
    przystanki = Przystanek.objects.filter(godzina__in=obj).order_by('godzina')
    # js = serializers.serialize('json', obj)


    for item_p in przystanki:
        #przystankiWszystkie():
        godz = []
        sobota = []
        powrot = []
        # roz['przystanek_' + str(item_p.id)] = item_p.nazwa
        # parametr 2 oznacza wszystkie godziny odjazdów
        for item_g in godz_odj_rozklad(2):
            if item_p.id == item_g.przystanek_id:
                godz.append(str(item_g.godzina)[0:5])
                sobota.append(item_g.godziny_sobota)
                powrot.append(item_g.powrot)
                rozklad[item_p.nazwa] = {
                    'id': item_p.id,
                    'opis': item_p.opis,
                    'odjazd': {
                        'godzina': odjazdyMeta(item_g.przystanek_id, czy_powrot),
                        'sobota': sobota,
                        'powrot': powrot,

                    }

                }

    etykieta_minuty = []

    for item in godziny:
        # minuty do tabeli rozkła
        temp_min = str(item.godzina)[3:5]
        etykieta_minuty.append(temp_min)

    return render(request, 'jazda/rozklad.html', {
        'przystanki': przystankiWszystkie(),
        'godziny': godziny,
        'godz_od_do_all': godziny_jazdy(2),
        'ety_godz_szek': godziny_jazdy(0),
        'ety_godz_powrot': godziny_jazdy(1),
        'godziny_lists': godziny_lists,
        'etykieta_minuty': etykieta_minuty,
        'obj': obj,
        'godz': rozkladDB(),
        'roz_szek': rozklad_szek(),
        'roz_powrot': rozklad_powrot(),
        'rozklad': rozklad,
        'colspan_len': len(godziny_jazdy(1)) + 1,
        # 'godzinki': odjazdy(1, '05:00'),
        #'slownik': odjazdyMeta(item_g.przystanek_id),

    }
                  )


# każdy kolejny widok-strona musi mieć tu swoją funkcje
def druga(request):
    return HttpResponse('Druga strona aplikacji')

def drive_challenge_by_number(request, desire):
    pages = list(content.keys())
    redirect_page = pages[desire - 1]
    redirect_path = reverse('drive-challenge', args=[redirect_page])
    return HttpResponseRedirect(redirect_path)

def drive_challenge(request, desire):
    try:
        odp = content[desire]
        # dla template
        return render(request, 'jazda/jazda.html', {
            'text': odp,
        })
        # dla template inaczej
        #odp = render_to_string('jazda/jazda.html')
    except:
        return HttpResponseNotFound('Taki content nie istnieje 404')
    #return  HttpResponse(odp)