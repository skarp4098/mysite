from jazda.views.rozklady import rozklad_www
from django.shortcuts import render

# powroty do skotnik ze szczecinka dlatego miasto_id to 2
def skotniki(request):
    miasto_id = 2
    powrot = 1

    return render(request, 'jazda/skotniki.html', {
                                              # 0 to sobota
        'rozklad_powrot': rozklad_www(powrot, 0, miasto_id),
        'kierunek': 'Skotnik',
    }
    )

