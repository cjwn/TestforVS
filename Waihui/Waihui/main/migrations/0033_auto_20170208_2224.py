# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-08 14:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_order_sku_topic_buyer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='sku_topic_buyer',
            new_name='sku_topic',
        ),
    ]
