# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_sku_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='gender',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'\xe7\x94\xb7'), (2, b'\xe5\xa5\xb3')]),
        ),
        migrations.AddField(
            model_name='buyer',
            name='provider',
            field=models.ForeignKey(default=1, to='main.Provider'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buyer',
            name='brithday',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='mother_tongue',
            field=models.ForeignKey(blank=True, to='main.Language', null=True),
        ),
        migrations.AlterField(
            model_name='provider',
            name='weekday_pattern',
            field=models.CommaSeparatedIntegerField(max_length=200, null=True, blank=True),
        ),
    ]
