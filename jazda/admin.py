from django.contrib import admin

# Register your models here.
from .models import Przystanek, Godzina, Rozklad, Miasto # Lokalizacja

from django.contrib import admin

#from django_google_maps import widgets as map_widgets
#from django_google_maps import fields as map_fields


# hybrid roadmap satellite terrain
# @admin.register(Lokalizacja)
# class LokalizacjaAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         map_fields.AddressField: {
#           'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
#     }
#     list_display = ('address', 'geolocation')


@admin.register(Miasto)
class MiastoAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'opis')
    fieldsets = (
        ('Pole obowiązkowe', {
            # 'description': "",
            'fields': ['nazwa']
        }),
        ('Dodatkowe informacje', {
            'classes': ('expand',),
            'fields': ['opis']
        }),
    )


@admin.register(Rozklad)
class RozkladAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'od', 'do', 'na_stronie')
    fieldsets = (
        ('Pola obowiązkowe', {
            # 'description': "",
            'fields': (('nazwa'), ('od', 'do'))
        }),
        ('Dodatkowe informacje', {
            'classes': ('expand',),
            'fields': ('na_stronie', 'description')
        }),
    )


@admin.register(Przystanek)
class PrzystanekAdmin(admin.ModelAdmin):
   # fields = ['miasto', 'nazwa', 'dlugosc', 'szerokosc', 'opis','opis_drugi' ]
    list_display = ('nazwa', 'opis', 'opis_drugi', 'miasto')
    fieldsets = (
        ('Pola obowiązkowe', {
            # 'description': "",
            'fields': (('nazwa', 'miasto'), ('dlugosc', 'szerokosc'))
        }),
        ('Dodatkowe informacje', {
            'classes': ('expand',),
            'fields': ('opis', 'opis_drugi')
        }),
    )


@admin.register(Godzina)
class GodzinaAdmin(admin.ModelAdmin):
    list_display = ('godzina', 'przystanek', 'powrot', 'sobota', 'zjazd_do_skotnik', 'rozklad')
    list_filter = ('przystanek', 'rozklad', 'powrot', 'sobota', 'zjazd_do_skotnik')
    fieldsets = (
        ('Pola obowiązkowe', {
           # 'description': "",
            'fields': (('rozklad', 'przystanek'), 'godzina')
        }),
        ('Dodatkowe informacje', {
            'classes': ('expand',),
            'fields': ('powrot', 'zjazd_do_skotnik', 'sobota')
        }),
    )



# admin.site.register(Przystanek)
# admin.site.register(Godzina)
# admin.site.register(Rozklad)



# admin.site.register(Rozklad, RozkladAdmin)
# admin.site.register(Godzina, GodzinaAdmin)
# admin.site.register(Przystanki, PrzystanekAdmin)



