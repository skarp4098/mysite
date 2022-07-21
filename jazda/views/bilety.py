from django.shortcuts import render

def bilety(request):

    return  render(request, 'jazda/bilety.html')