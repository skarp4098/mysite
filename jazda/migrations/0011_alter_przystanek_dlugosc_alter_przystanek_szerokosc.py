# Generated by Django 4.0.4 on 2022-08-05 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jazda', '0010_przystanek_dlugosc_przystanek_szerokosc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='przystanek',
            name='dlugosc',
            field=models.FloatField(blank=True, default=False, verbose_name='Dł. geograficzna'),
        ),
        migrations.AlterField(
            model_name='przystanek',
            name='szerokosc',
            field=models.FloatField(blank=True, default=False, verbose_name='Szer. geograficzna'),
        ),
    ]
