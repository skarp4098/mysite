from django.shortcuts import render
from jazda.views.rozklady import rozklad_www

def gwda(request):
    miasto_id = 3


    return render(request, 'jazda/gwda.html',{

        'rozklad_tam': rozklad_www(0, 0, miasto_id),
        'kierunek': 'CZARNE',
        'rozklad_powrot': rozklad_www(1, 0, miasto_id),
        'kierunek_powrot': 'Szczecinek >> Skotniki',

    }
    )