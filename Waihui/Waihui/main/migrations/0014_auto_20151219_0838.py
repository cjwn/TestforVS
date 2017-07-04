# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20151212_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.IntegerField(default=0, choices=[(0, b'unread'), (1, b'read')]),
        ),
    ]
