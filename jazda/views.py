from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from  django.urls import reverse
from  django.shortcuts import render


def index(request):

    return render(request, 'jazda/index.html' )

# def druga(request):
#     return HttpResponse('Druga strona aplikacji')
#
# def drive_challenge_by_number(request, desire):
#     pages = list(content.keys())
#     redirect_page = pages[desire - 1]
#     redirect_path = reverse('drive-challenge', args=[redirect_page])
#     return HttpResponseRedirect(redirect_path)
#
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