# Generated by Django 4.0.4 on 2022-08-05 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jazda', '0013_alter_godzina_rozklad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rozklad',
            name='do',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='rozklad',
            name='od',
            field=models.DateField(),
        ),
    ]
