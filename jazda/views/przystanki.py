from django.shortcuts import render
from jazda.models import Rozklad, Miasto, Godzina, Przystanek

def make_url(przyst_id, przystanki):
    tam = []
    powrot = []
    paczka_url = []
    url = "przystanek/"
    godzina_items = Godzina.objects.filter(przystanek_id=przyst_id)
    przystanek = przystanki.filter(id=przyst_id)

    for item in godzina_items:
        if item.powrot == 0 and przyst_id not in tam:
            tam.append(przyst_id)
        elif item.powrot == 1 and przyst_id not in powrot:
            powrot.append(przyst_id)

    for item in przystanek:
        # jeśli z jednego przystanku autobus jeździ w obu kierunkach
        if przyst_id in tam and przyst_id in powrot:
            temp1 = url + str(przyst_id)  + '0'
            paczka_url.append(temp1)
            temp2 = url + str(przyst_id)  + '1'
            paczka_url.append(temp2)
        # odjazdy
        if przyst_id in tam:
            url = url  + str(przyst_id)  + '0'
        # powroty
        if przyst_id in powrot:
            url = url  + str(przyst_id)  + '1'
    # url tam i powrot w liście []
    if len(paczka_url) > 1:
        return paczka_url
    else:
        return url

def przyst(miasto_id=0):
    slownik_przystankow = {}
    przystanki = Przystanek.objects.filter(miasto_id=miasto_id).order_by('nazwa')
    godziny = Godzina.objects.filter()
    for item_p in przystanki:
        etykieta = item_p.nazwa + ', ' + item_p.opis
        slownik_przystankow[etykieta] = {
            #'id_przyst': item_p.id,
            'url': make_url(item_p.id, przystanki),

        }
    return slownik_przystankow


def miasto(miasto_id=0):
    slownik_miasto = {}

    if miasto_id == 0:
        miasta = Miasto.objects.all()
        for item_m in miasta:
            slownik_miasto[item_m.nazwa] = {
                'id_miasta': item_m.id,
                'przystanki': przystanki(int(item_m.id))

            }

    else:
        miasta = Miasto.objects.filter(id=miasto_id)
        for item_m in miasta:
            slownik_miasto[item_m.nazwa] = {
                'id_miasta': item_m.id,
                'przystanki': przyst(item_m.id)

            }

    return slownik_miasto


def rozklad(miasto_id=0):
    slownik_rozklad = {}
    rozklady = Rozklad.objects.filter(na_stronie__exact=1)

    # godzina_items = Godzina.objects.filter(rozklad_id__in=rozklady, przystanek_id__in=przystanki).order_by('przystanek_id')

    for item_r in rozklady:
        slownik_rozklad[item_r.nazwa] = {
        'od': str(item_r.od),
        'miasto': miasto(miasto_id),

        }
    return slownik_rozklad


def przystanki(request):

    return render(request, 'jazda/przystanki.html',{
       # 'kolekcja': rozklad(),
        'skotniki': rozklad(1),
        'szczecinek': rozklad(2),
        'gwda': rozklad(3),
        'czarne': rozklad(4)

    }
    )