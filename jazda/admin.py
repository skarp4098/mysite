from django.contrib import admin

# Register your models here.
from .models import Przystanek, Godzina, Rozklad, Miasto

@admin.register(Miasto)
class MiastoAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'opis')

@admin.register(Rozklad)
class RozkladAdmin(admin.ModelAdmin):
    list_display = ('nazwa', 'od', 'do', 'na_stronie')


@admin.register(Przystanek)
class PrzystanekAdmin(admin.ModelAdmin):
    fields = ['miasto', 'nazwa', 'opis', 'opis_drugi' ]
    list_display = ('nazwa', 'opis', 'opis_drugi', 'miasto')


@admin.register(Godzina)
class GodzinaAdmin(admin.ModelAdmin):
    list_display = ('godzina', 'przystanek', 'powrot', 'sobota', 'zjazd_do_skotnik', 'rozklad')
    list_filter = ['przystanek']


# admin.site.register(Przystanek)
# admin.site.register(Godzina)
# admin.site.register(Rozklad)



# admin.site.register(Rozklad, RozkladAdmin)
# admin.site.register(Godzina, GodzinaAdmin)
# admin.site.register(Przystanki, PrzystanekAdmin)



