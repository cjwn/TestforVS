# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-18 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minutes', '0010_auto_20161018_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='attended_entries',
            field=models.ManyToManyField(to='minutes.Entry', verbose_name='\u51fa\u5e2d\u7684\u4f1a\u8bae'),
        ),
    ]
