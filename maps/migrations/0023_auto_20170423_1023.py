# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-23 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0022_auto_20170422_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='osm_id',
            field=models.PositiveIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='wikidata_id',
            field=maps.fields.ExternalIdField(max_length=15, null=True),
        ),
    ]
