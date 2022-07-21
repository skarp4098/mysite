from django.shortcuts import render
from jazda.views.rozklady import rozklad_www

def gwdapowrot(request):
    miasto_id = 3

    return render(request, 'jazda/gwdapowrot.html',{

        'rozklad_powrot': rozklad_www(1, 0, miasto_id),
        'kierunek': 'Szczecinek >> Skotniki',

    }
    )