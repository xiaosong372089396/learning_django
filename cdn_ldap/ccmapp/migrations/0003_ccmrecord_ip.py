# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-05-27 05:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccmapp', '0002_auto_20170527_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='ccmrecord',
            name='ip',
            field=models.GenericIPAddressField(db_index=True, null=True, protocol='ipv4'),
        ),
    ]
