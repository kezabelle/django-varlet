# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-11-07 22:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=2048, unique=True, verbose_name='url')),
                ('template', models.CharField(help_text='templates may affect the display of this page on the website.', max_length=255, verbose_name='template')),
            ],
            options={
                'swappable': 'VARLET_PAGE_MODEL',
            },
        ),
    ]
