# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-04-10 08:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u90e8\u95e8\u540d')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u90e8\u95e8\u9886\u5bfc')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u90e8\u95e8',
                'verbose_name_plural': '\u90e8\u95e8\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u59d3\u540d')),
                ('role_type', models.IntegerField(choices=[(1, '\u666e\u901a\u4eba\u5458'), (2, '\u8fd0\u7ef4\u4eba\u5458'), (3, '\u7ba1\u7406\u4eba\u5458')], default=1, verbose_name='\u6743\u9650\u7c7b\u578b')),
                ('head_img', models.ImageField(blank=True, null=True, upload_to='static/userimg', verbose_name='\u5934\u50cf')),
                ('privilege', models.IntegerField(choices=[(1, '\u666e\u901a'), (2, '\u4e2d\u7ea7'), (3, '\u9ad8\u7ea7'), (4, '\u8d85\u7ea7')], default=1, verbose_name='\u6743\u9650')),
                ('is_login', models.BooleanField(default=False, verbose_name='\u662f\u5426\u767b\u5f55')),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('mail', models.CharField(max_length=80, verbose_name='\u90ae\u7bb1')),
                ('cell', models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7')),
                ('send_alarm', models.BooleanField(default=False, verbose_name='\u662f\u5426\u53d1\u9001\u62a5\u8b66')),
                ('memo', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u5907\u6ce8')),
                ('modify_time', models.DateTimeField(auto_now=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Department')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u9644\u52a0\u7528\u6237\u4fe1\u606f',
                'verbose_name_plural': '\u9644\u52a0\u7528\u6237\u4fe1\u606f\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='\u540d\u79f0')),
                ('alias', models.CharField(max_length=32, verbose_name='\u522b\u540d')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': '\u89d2\u8272',
                'verbose_name_plural': '\u89d2\u8272\u5217\u8868',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Role', verbose_name='\u89d2\u8272'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
