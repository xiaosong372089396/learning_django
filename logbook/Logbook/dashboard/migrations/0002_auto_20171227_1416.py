# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-27 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shanxi',
            name='HostId',
            field=models.IntegerField(verbose_name='\u4e3b\u673aId'),
        ),
        migrations.AlterField(
            model_name='shanxi',
            name='status',
            field=models.IntegerField(verbose_name='\u4e3b\u673a\u72b6\u6001'),
        ),
    ]