# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('menu_title', models.CharField(help_text='may be displayed in menus, instead of the standard title', max_length=255, verbose_name='menu title', blank=True)),
                ('is_homepage', models.BooleanField(default=False, db_index=True)),
                ('slug', models.SlugField(help_text='a human and search engine friendly name for this object. Only mixed case letters, numbers and dashes are allowed. Once set, this cannot be changed.', unique=True, max_length=255, verbose_name='friendly URL')),
                ('template', models.CharField(help_text='templates may affect the display of this page on the website.', max_length=255, verbose_name='template', db_index=True)),
            ],
            options={
                'db_table': 'varlet_page',
            },
            bases=(models.Model,),
        ),
    ]
