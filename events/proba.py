from django.db import models
from jazda.models import Rozklad, Przystanek, Godzina

godzina_list = Godzina.objects.all()
print(godzina_list)