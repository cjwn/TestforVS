# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20151219_0839'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='desc',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='skus',
            field=models.ManyToManyField(to='main.Sku', blank=True),
        ),
    ]
