import datetime
import time

from django.db import models
# from django_google_maps import fields as map_fields

# from django.conf import settings

# Create your models here.

# class Lokalizacja(models.Model):
#     address = map_fields.AddressField('Adres', max_length=200)
#     geolocation = map_fields.GeoLocationField('Namiary', max_length=100)
#
#     def __str__(self):
#         return f'{self.address}'
#
#     class Meta:
#         verbose_name_plural = 'lokalizacje'


class Miasto(models.Model):
    nazwa = models.CharField('Nazwa miasta', max_length=50)
    opis = models.CharField('Opis miasta', max_length=100, blank=True)

    def __str__(self):
        return f'{self.nazwa}'

    class Meta:
        verbose_name_plural = 'miasta'



class Przystanek(models.Model):
    nazwa = models.CharField('Nazwa przystanku',max_length=100)
    miasto = models.ForeignKey(Miasto, on_delete=models.CASCADE)
    dlugosc = models.FloatField('Dł. geograficzna', blank=False)
    szerokosc = models.FloatField('Szer. geograficzna', blank=False)
    opis = models.CharField('Opis', max_length=100, blank=True)
    opis_drugi = models.CharField('Dodatkowy opis', max_length=200, blank=True)

    def __str__(self):
        return f'{self.nazwa}, {self.opis}'

    class Meta:
        verbose_name_plural = 'przystanki'
        ordering = ['miasto']


class Rozklad(models.Model):

    nazwa = models.CharField('Nazwa rozkładu',max_length=100)
    od = models.DateField(blank=False)
    do = models.DateField(blank=False)
    na_stronie = models.BooleanField('Aktualnie w internecie', default=False)
    description = models.TextField('Komentarz', blank=True)

    class Meta:
        verbose_name_plural = 'rozkłady'

    def __str__(self):
        return f'{self.nazwa} {self.od} {self.do}'


class Godzina(models.Model):

    godzina = models.TimeField('Godzina')
    przystanek = models.ForeignKey(Przystanek, on_delete=models.CASCADE)
    rozklad = models.ForeignKey(Rozklad, on_delete=models.CASCADE)
    powrot = models.BooleanField('powrót', default=False, blank=True)
    zjazd_do_skotnik = models.BooleanField('zjazd do Skotnik', default=False)
    sobota = models.BooleanField(default=False, verbose_name='kursuje w soboty')


    def __str__(self):
        return f'{self.godzina}'

    class Meta:
        verbose_name_plural = 'godziny'
        ordering = ['godzina']