# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-18 14:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0006_country_sparql'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('language_code', models.CharField(db_index=True, max_length=15)),
            ],
            options={
                'db_tablespace': '',
                'db_table': 'maps_country_translation',
                'abstract': False,
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.AlterModelManagers(
            name='country',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('_plain_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='country',
            name='name',
        ),
        migrations.AddField(
            model_name='countrytranslation',
            name='master',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='maps.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='countrytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]