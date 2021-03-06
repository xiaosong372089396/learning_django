# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-21 07:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('txnetworks', '0003_auto_20170620_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='txnetwork',
            name='active',
        ),
        migrations.AddField(
            model_name='txnetwork',
            name='flushpath',
            field=models.CharField(max_length=20, null=True, verbose_name='\u70ed\u66f4\u8def\u5f84'),
        ),
        migrations.AddField(
            model_name='txnetwork',
            name='flushurl',
            field=models.URLField(null=True, verbose_name='\u70ed\u66f4\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='txnetwork',
            name='date',
            field=models.CharField(max_length=32, null=True, verbose_name='\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='txnetwork',
            name='username',
            field=models.CharField(max_length=32, null=True, verbose_name='\u7528\u6237'),
        ),
    ]
