from django.shortcuts import render
from jazda.views.rozklady import rozklad_www
from jazda.views.etykiety import etykiety


def soboty(request):

    return render(request, 'jazda/soboty.html',{
                'ety_przystanki': 'przystanki', # etykiety(0),
                'kierunek_tam': 'Skotniki >> Szczecinek >> Gwda >> Czarne',
                'kierunek_powrot': 'Czarne >> Gwda >> Szczecinek >> Skotniki',
                'rozklad_sobota': rozklad_www(0, 1),
                'rozklad_sobota_powrot': rozklad_www(1, 1),

    }
    )