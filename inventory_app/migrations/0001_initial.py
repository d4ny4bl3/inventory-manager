# Generated by Django 5.1.1 on 2024-09-05 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shelf', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Rack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('total_shelf', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('product_id', models.CharField(db_index=True, max_length=20)),
                ('url', models.URLField()),
                ('is_active', models.BooleanField(default=True)),
                ('is_check', models.BooleanField(default=True)),
                ('location', models.ManyToManyField(blank=True, null=True, to='inventory_app.location')),
            ],
        ),
        migrations.AddField(
            model_name='location',
            name='rack',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.rack'),
        ),
        migrations.AddField(
            model_name='location',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory_app.room'),
        ),
    ]
