from django.urls import  path
from . import views

app_name = 'jazda'
urlpatterns = [

    path('', views.index, name='index'),
    # path('rozklad/', views.rozklad, name='rozklad'),
    # dla parametru int; kolejność taka jak we views.py
    path('przystanek/<int:value_id><int:powrot>', views.przystanek, name='przystanek'),
    path('przystanki/', views.przystanki, name='przystanki'),
    path('skotniki/', views.skotniki, name='skotniki'),
    path('szczecinek/', views.szczecinek, name='szczecinek'),
    path('gwda/', views.gwda, name='gwda'),
    path('gwdapowrot/', views.gwdapowrot, name='gwdapowrot'),
    path('czarne/', views.czarne, name='czarne'),
    path('soboty/', views.soboty, name='soboty'),
    path('ulgi/', views.ulgi, name='ulgi'),
    path('oferta/', views.oferta, name='oferta'),
    path('bilety/', views.bilety, name='bilety'),
    path('galeria/', views.galeria, name='galeria'),

    # dla parametru string
    # path('<str:desire>', views.drive-challenge, name='drive-challenge'),
    #path('<str:desire>', OdjazdyListView.as_view(), name='drive-challenge')

]