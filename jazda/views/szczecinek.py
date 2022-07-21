from django.shortcuts import get_object_or_404
from jazda.views.rozklady import rozklad_www
from jazda.models import Rozklad, Przystanek, Miasto, Godzina
from django.shortcuts import render

# def content(id_miasta=0):
#     lista = []
#     rozklad_items = Rozklad.objects.filter(na_stronie__exact=1)
#     godzina = Godzina.objects.filter(rozklad_id__in=rozklad_items)
#     przystanek = Przystanek.objects.filter(miasto_id=id_miasta, godzina__in=godzina ).order_by('nazwa')
#
#     for item in przystanek:
#         if item.id not in lista:
#             lista.append(item.id)
#
#     return lista



def szczecinek(request):
    miasto_id = 2
    return render(request, 'jazda/szczecinek.html', {

    'rozklad_tam': rozklad_www(0, 0, miasto_id),
    'kierunek': 'GWDA >> CZARNE',
    # 'slownik': content(2)

    }
    )