# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-11 16:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0004_auto_20160327_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extuser',
            name='avatar',
            field=models.ForeignKey(default='avatars/avatar.png', on_delete=django.db.models.deletion.CASCADE, to='avatar.Avatar'),
        ),
    ]