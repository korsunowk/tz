# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-29 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0004_auto_20160327_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extuser',
            name='avatar',
            field=models.ImageField(blank=True, default='avatars/avatar.png', null=True, upload_to='avatars/'),
        ),
    ]
