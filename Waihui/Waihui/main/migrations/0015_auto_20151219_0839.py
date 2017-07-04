# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20151219_0838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='skus',
        ),
        migrations.AddField(
            model_name='order',
            name='skus',
            field=models.ManyToManyField(to='main.Sku', null=True, blank=True),
        ),
    ]
