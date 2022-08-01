from jazda.models import Przystanek, Godzina, Rozklad

def ilosc_przystankow(id_rozkl, powrot, sobota=0, miasto_id=0):
    lista = []

    godzina_items = Godzina.objects.filter(rozklad_id=id_rozkl, powrot=powrot )

    # dla strony soboty.html
    if sobota > 0:
        godzina_items = Godzina.objects.filter(rozklad_id=id_rozkl, powrot=powrot, sobota=sobota)
        przystanek_items = Przystanek.objects.filter(godzina__in=godzina_items)

    else:
        przystanek_items = Przystanek.objects.filter(godzina__in=godzina_items, miasto_id=miasto_id)

    for item_p in przystanek_items:
        if item_p.nazwa not in lista:
            lista.append(item_p.nazwa)
    return len(lista)

def ilosc_przystankow2(id_rozkl, powrot, sobota=0, miasto_id=0):
    lista = []
    godzina_items = Godzina.objects.filter(rozklad_id=id_rozkl, powrot=powrot)

    # dla strony soboty.html
    if sobota > 0:
        godzina_items = Godzina.objects.filter(rozklad_id=id_rozkl, powrot=powrot, sobota=sobota
                                               )
    przystanek_items = Przystanek.objects.filter(godzina__in=godzina_items, miasto_id=miasto_id)

    for item_p in przystanek_items:
        if item_p.id not in lista:
            lista.append(item_p.id)
    return lista



def odjazdy_wszystkie(przyst_id, rozkl_id, powrot, godzina):
    """Funkcja ustala godziny odjazdów w zbiorczym rozkładzie jazdy"""
    odjazdy = []
    jeden_odjazd = ''

    godzina_items = Godzina.objects.filter(powrot=powrot, rozklad_id=rozkl_id, przystanek_id=przyst_id,
                                    godzina__startswith=godzina)  # .order_by('przystanek_id')

    for item in godzina_items:
        if item.sobota and item.zjazd_do_skotnik:
            odjazdy.append(str(item)[3:5] + "'sz ")  #[0:5] hh:mm   [3:5] mm
            jeden_odjazd = str(item)[3:5] + "'sz "
        elif item.zjazd_do_skotnik:
            odjazdy.append(str(item)[3:5] + "'z ")
            jeden_odjazd = str(item)[3:5] + "'z "
        elif item.sobota:
            odjazdy.append(str(item)[3:5] + "'s ")
            jeden_odjazd = str(item)[3:5] + "'s "
        else:
            odjazdy.append(str(item)[3:5] + "' ")
            jeden_odjazd = str(item)[3:5]  + "' "

    if len(odjazdy) > 1:
        return odjazdy
    else:
        return jeden_odjazd

def godziny_dni_powszednie(przyst_id, rozkl_id, powrot, godzina):
    """Funkcja dla pliku przystanek.html"""
    odjazdy = []
    jeden_odjazd = ''
    godziny_powszednie = Godzina.objects.filter(przystanek_id=przyst_id, rozklad_id=rozkl_id,
                                        powrot=powrot, godzina__startswith=str(godzina)[0:2])

    for item in godziny_powszednie:
        if not item.sobota:
            odjazdy.append(str(item)[3:5]) # + "' ")
            jeden_odjazd = str(item)[3:5] # + "' "

    if len(odjazdy) > 1:
        return odjazdy
    else:
        return jeden_odjazd

def godziny_sobota(przyst_id, rozkl_id, powrot, godzina):
    """Funkcja dla strony przystanek.html"""
    odjazdy_sobota = []
    godz_sobota = Godzina.objects.filter(przystanek_id=przyst_id, rozklad_id=rozkl_id, sobota=1,
                                    powrot=powrot, godzina__startswith=str(godzina)[0:2])
    jeden_odjazd = ''

    for item in godz_sobota:
        if item.sobota and item.zjazd_do_skotnik:
            odjazdy_sobota.append(str(item)[3:5] + "'z ")
            jeden_odjazd = str(item)[3:5] + "'z "
        elif item.sobota:
            odjazdy_sobota.append(str(item)[3:5] + "' ")
            jeden_odjazd = str(item)[3:5] + "' "

    if len(odjazdy_sobota) > 1:
        return odjazdy_sobota
    else:
        return jeden_odjazd

def przystanek_odjazdy(przyst_id, rozkl_id, powrot, sobota=0, miasto_id=0):
    """Funkcja ustala godziny odjazdów dla przystanku"""
    slownik = {}
    etykiety = etykiety_godzin_th(rozkl_id, powrot, 0, 0, miasto_id)

    if sobota > 0:
        etykiety = etykiety_godzin_th(rozkl_id, powrot, 0, sobota)
        for item_g in etykiety:
            slownik[str(item_g)[0:2]] = {
                'sobota': godziny_sobota(przyst_id, rozkl_id, powrot, item_g)
            }
    else:
        for item_g in etykiety:
            # sprawdzenie dla każdej etykiety_th
                slownik[str(item_g)[0:2]] = {
                    'min': odjazdy_wszystkie(przyst_id, rozkl_id, powrot, item_g),
                   # 'daily': godziny_dni_powszednie(przyst_id, rozkl_id, powrot, item_g),
                   # 'sobota': godziny_sobota(przyst_id, rozkl_id, powrot, item_g)
                }

    return slownik

def etykiety_godzin_th(rozklad_id, powrot=0, przyst_id=0, sobota=0, miasto_id=0):
    """Funkcja przygotowuje etykiety pełnych godzin dla poszczególnych kolumn <th> rozkładu jazdy"""
    etykieta_godziny = []
    przystanki_items = Przystanek.objects.filter(miasto_id=miasto_id)

    # dla strony soboty.html
    if sobota > 0:
        godziny = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot, sobota=sobota).order_by('godzina')
    # dla strony przystanek.html
    elif przyst_id > 0 and sobota == 0:
        godziny = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot, przystanek_id=przyst_id).order_by('godzina')
    # dla wszystkich przystanków
    else:
        godziny = Godzina.objects.filter(rozklad_id=rozklad_id, powrot=powrot,
                                   przystanek_id__in=przystanki_items).order_by('godzina')

    for item in godziny:
        # przycięta do pełnej, godzina z DB
        temp_godz = str(item.godzina)[0:2]
        # zapisuje tylko jedno wystąpienie danej godziny
        if temp_godz not in etykieta_godziny:
            etykieta_godziny.append(temp_godz)

    return etykieta_godziny

def przystanki_info(id_rozkl, powrot, sobota=0, miasto_id=0):
    slownik2 = {}

    godzina_items = Godzina.objects.filter(rozklad_id=id_rozkl, powrot=powrot)

    # dla strony soboty.html
    if sobota > 0:
        godzina_items = Godzina.objects.filter(rozklad_id=id_rozkl, powrot=powrot, sobota=sobota)
        przystanek_items = Przystanek.objects.filter(godzina__in=godzina_items).order_by('godzina')

    elif powrot > 0:
        przystanek_items = Przystanek.objects.filter(godzina__in=godzina_items, miasto_id=miasto_id).order_by('godzina', 'id')
    else:
        przystanek_items = Przystanek.objects.filter(godzina__in=godzina_items, miasto_id=miasto_id).order_by('id', 'godzina')

    for item_p in przystanek_items:
        slownik2[item_p.nazwa] = {
            'id': item_p.id,
            'opis': item_p.opis,
            'opis2': item_p.opis_drugi,
            'godzina': przystanek_odjazdy(item_p.id, id_rozkl, powrot, sobota, miasto_id)

        }
    return slownik2


def rozklad_www(powrot=0, sobota=0, miasto_id=0):
    slownik1 = {}

    rozklad_items = Rozklad.objects.filter(na_stronie__exact=1)

    if sobota > 0:
        for item_r in rozklad_items:   # parametr 0 robi za przyst_id i tu ma być 0
            etykiety = etykiety_godzin_th(item_r.id, powrot, 0, sobota)
            liczba_przy = ilosc_przystankow(item_r.id, powrot, sobota)
            # odjazdy =
            slownik1[item_r.nazwa] = {
                'od': str(item_r.od),
                'do': str(item_r.do),
                'desc': item_r.description,
                'etykiety_godzin': etykiety,
                'liczba_przyst': liczba_przy,
                'przystanek': przystanki_info(item_r.id, powrot, sobota)
            }
    else:
        for item_r in rozklad_items:
            etykiety = etykiety_godzin_th(item_r.id, powrot, 0, 0, miasto_id)
            liczba_przy = ilosc_przystankow(item_r.id, powrot, 0, miasto_id)
           # odjazdy =
            slownik1[item_r.nazwa] = {
                'od': str(item_r.od),
                'do': str(item_r.do),
                'desc': item_r.description,
                'etykiety_godzin': etykiety,
                'liczba_przyst': liczba_przy,
                'przystanek': przystanki_info(item_r.id, powrot, 0, miasto_id),
               # 'blad': ilosc_przystankow2(item_r.id, powrot, 0, miasto_id)
            }

    return slownik1