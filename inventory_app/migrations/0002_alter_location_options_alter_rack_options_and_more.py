# Generated by Django 5.1.1 on 2024-09-05 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'Umístění', 'verbose_name_plural': 'Umístění'},
        ),
        migrations.AlterModelOptions(
            name='rack',
            options={'verbose_name': 'Regál', 'verbose_name_plural': 'Regály'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'verbose_name': 'Místnost', 'verbose_name_plural': 'Místnosti'},
        ),
        migrations.AddField(
            model_name='rack',
            name='room',
            field=models.OneToOneField(default=5, on_delete=django.db.models.deletion.CASCADE, to='inventory_app.room'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='rack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.rack', verbose_name='Regál'),
        ),
        migrations.AlterField(
            model_name='location',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.room', verbose_name='Místnost'),
        ),
        migrations.AlterField(
            model_name='location',
            name='shelf',
            field=models.IntegerField(verbose_name='Police'),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Popis'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=10, unique=True, verbose_name='Označení'),
        ),
    ]
