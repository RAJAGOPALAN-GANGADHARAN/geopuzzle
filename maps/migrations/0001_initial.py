# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 22:50
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('difficulty', models.PositiveSmallIntegerField(choices=[(0, 'disabled'), (1, 'easy'), (2, 'normal'), (3, 'hard')], default=0)),
                ('polygon', django.contrib.gis.db.models.fields.MultiPolygonField(geography=True, srid=4326)),
                ('answer', django.contrib.gis.db.models.fields.MultiPointField(geography=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('slug', models.CharField(max_length=15)),
                ('center', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('position', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('zoom', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Country'),
        ),
    ]
