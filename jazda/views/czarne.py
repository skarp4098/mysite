from django.shortcuts import get_object_or_404
from jazda.views.rozklady import rozklad_www
from django.shortcuts import render


def czarne(request):
    miasto_id = 4
    return render(request, 'jazda/czarne.html', {
    'rozklad_powrot': rozklad_www(1, 0, miasto_id),
    'kierunek': 'Gwda >> Szczecinek >> Skotniki',

    }
    )