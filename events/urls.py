from django.urls import path, re_path
from . import  views


urlpatterns = [

    path('', views.index, name='index'),
    path('events/', views.all_events, name='showevents'),
    # path('rozklad/', views.rozklad, name='rozklad'),
    path('<int:year>/<str:month>/', views.index, name='index'),
    path('add_venue/', views.add_venue, name='add-venue'),
    path('tdemo/', views.template_demo, name='tdemo'),

]