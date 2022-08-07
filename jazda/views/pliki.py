from django.http.response import HttpResponse
from django.shortcuts import render

def pliki(request):

    return render(request, 'jazda/pliki.html')