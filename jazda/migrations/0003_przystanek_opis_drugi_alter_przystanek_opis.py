# Generated by Django 4.0.4 on 2022-06-22 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jazda', '0002_alter_godzina_rozklad'),
    ]

    operations = [
        migrations.AddField(
            model_name='przystanek',
            name='opis_drugi',
            field=models.CharField(blank=True, max_length=200, verbose_name='Dodatkowy opis'),
        ),
        migrations.AlterField(
            model_name='przystanek',
            name='opis',
            field=models.CharField(blank=True, max_length=100, verbose_name='Opis'),
        ),
    ]
