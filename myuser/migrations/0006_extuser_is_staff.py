# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-03 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0005_auto_20160929_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='extuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Is staff'),
        ),
    ]
