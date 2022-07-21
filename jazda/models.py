import datetime
import time

from django.db import models
# from django.conf import  settings

# Create your models here.

class Miasto(models.Model):
    nazwa = models.CharField('Nazwa miasta', max_length=50)
    opis = models.CharField('Opis miasta', max_length=100, blank=True)

    def __str__(self):
        return f'{self.nazwa}'

    class Meta:
        verbose_name_plural = 'miasta'



class Przystanek(models.Model):
    nazwa = models.CharField('Nazwa przystanku',max_length=100)
    opis = models.CharField('Opis', max_length=100, blank=True)
    opis_drugi = models.CharField('Dodatkowy opis', max_length=200, blank=True)
    miasto = models.ForeignKey(Miasto, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nazwa}, {self.opis}'

    class Meta:
        verbose_name_plural = 'przystanki'
        ordering = ['miasto']


class Rozklad(models.Model):

    nazwa = models.CharField('Nazwa rozkładu',max_length=100)
    na_stronie = models.BooleanField('Aktualnie w internecie',default=False)
    od = models.DateField(blank=True)
    do = models.DateField(blank=True)
    description = models.TextField('Komentarz', blank=True)

    class Meta:
        verbose_name_plural = 'rozkłady'

    def __str__(self):
        return f'{self.nazwa} {self.od} {self.do}'


class Godzina(models.Model):

    godzina = models.TimeField('Godzina')
    przystanek = models.ForeignKey(Przystanek, on_delete=models.CASCADE)
    rozklad = models.ForeignKey(Rozklad, on_delete=models.CASCADE, default=2)
    powrot = models.BooleanField('powrót', default=False, blank=True)
    zjazd_do_skotnik = models.BooleanField('zjazd do Skotnik', default=False)
    sobota = models.BooleanField(default=False, verbose_name='kursuje w soboty')


    def __str__(self):
        return f'{self.godzina}'

    class Meta:
        verbose_name_plural = 'godziny'
        ordering = ['godzina']