# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 05:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20170206_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
