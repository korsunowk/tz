# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=15, unique=True, verbose_name='Username')),
                ('email', models.EmailField(max_length=255, verbose_name='Email')),
                ('phone', models.IntegerField(verbose_name='Phone')),
                ('firstname', models.CharField(max_length=40, verbose_name='First name')),
                ('lastname', models.CharField(max_length=40, verbose_name='Last name')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'db_table': 'myuser',
                'verbose_name_plural': 'users',
            },
        ),
    ]
