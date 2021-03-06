# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-13 09:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='overseas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=32, verbose_name='\u65f6\u95f4')),
                ('username', models.CharField(max_length=32, verbose_name='\u7528\u6237')),
                ('ip', models.GenericIPAddressField(db_index=True, null=True, protocol='ipv4', verbose_name='IP\u5730\u5740')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u6d77\u5916\u7f13\u5b58',
                'verbose_name_plural': '\u6d77\u5916\u7f13\u5b58',
            },
        ),
    ]
