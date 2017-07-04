# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 12, 12, 17, 30, 314953, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 12, 12, 17, 46, 483417, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.IntegerField(default=0, choices=[(0, b'unread'), (1, b'readed')]),
        ),
    ]
