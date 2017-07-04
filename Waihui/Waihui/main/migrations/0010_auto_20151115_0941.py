# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20151107_0440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sku',
            name='roomlink',
        ),
        migrations.AddField(
            model_name='plan',
            name='roomlink',
            field=models.URLField(null=True),
        ),
    ]
