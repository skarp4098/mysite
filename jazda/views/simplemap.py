import os
from django.http.response import HttpResponse
from django.shortcuts import render
from django.conf import settings

def simplemap(request):

    context = {
        "google_api_key": settings.GOOGLE_MAPS_API_KEY,
        'dlugosc': 53.71289173371238,
        'szerokosc': 16.679715908088138,

    }

    return render(request, 'jazda/simplemap.html', context)