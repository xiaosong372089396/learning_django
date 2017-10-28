# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-16 02:35
from __future__ import unicode_literals

import account.tools
import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='Username')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('email', models.EmailField(max_length=30, verbose_name='Email')),
                ('role', models.CharField(blank=True, choices=[(b'Admin', 'Administrator'), (b'User', 'User'), (b'App', 'Application'), (b'Proj', 'Project')], default=b'User', max_length=10, verbose_name='Role')),
                ('avatar', models.ImageField(null=True, upload_to=b'avatar', verbose_name='Avatar')),
                ('wechat', models.CharField(blank=True, max_length=30, verbose_name='Wechat')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('enable_otp', models.BooleanField(default=False, verbose_name='Enable OTP')),
                ('comment', models.TextField(blank=True, max_length=200, verbose_name='Comment')),
                ('is_first_login', models.BooleanField(default=False)),
                ('date_expired', models.DateTimeField(blank=True, default=account.tools.date_expired_default, null=True)),
                ('created_by', models.CharField(default=b'', max_length=30, verbose_name='Created by')),
            ],
            options={
                'ordering': ['username'],
                'verbose_name': '\u7528\u6237',
                'verbose_name_plural': '\u7528\u6237',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='LoginLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='Username')),
                ('name', models.CharField(blank=True, max_length=20, verbose_name='Name')),
                ('login_ip', models.GenericIPAddressField(verbose_name='Login ip')),
                ('login_city', models.CharField(blank=True, max_length=254, null=True, verbose_name='Login city')),
                ('user_agent', models.CharField(blank=True, max_length=254, null=True, verbose_name='User agent')),
                ('date_login', models.DateTimeField(auto_now_add=True, verbose_name='Date login')),
            ],
            options={
                'ordering': ['-date_login', 'username'],
                'db_table': 'login_log',
                'verbose_name': '\u767b\u5f55\u65e5\u5fd7',
                'verbose_name_plural': '\u767b\u5f55\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_discard', models.BooleanField(default=False, verbose_name='is discard')),
                ('discard_time', models.DateTimeField(blank=True, null=True, verbose_name='discard time')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name=b'\xe9\x83\xa8\xe9\x97\xa8\xe5\x90\x8d')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date created')),
                ('created_by', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u90e8\u95e8',
                'verbose_name_plural': '\u90e8\u95e8',
            },
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, null=True, related_name='users', to='account.UserGroup', verbose_name='User group'),
        ),
        migrations.AddField(
            model_name='user',
            name='project',
            field=models.ManyToManyField(blank=True, null=True, to='account.Project', verbose_name='Project'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]