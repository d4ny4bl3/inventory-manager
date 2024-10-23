# Generated by Django 5.1.1 on 2024-09-14 21:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_app', '0005_alter_product_options_remove_location_room_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='shelf',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)], verbose_name='Police'),
        ),
        migrations.AlterField(
            model_name='product',
            name='location',
            field=models.ManyToManyField(blank=True, to='inventory_app.location', verbose_name='Umístění'),
        ),
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='rack',
            name='number',
            field=models.IntegerField(verbose_name='Číslo regálu'),
        ),
    ]
