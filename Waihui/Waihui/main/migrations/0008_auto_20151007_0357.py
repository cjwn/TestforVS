# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150815_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sku',
            name='buyer',
            field=models.ManyToManyField(to='main.Buyer', blank=True),
        ),
    ]
