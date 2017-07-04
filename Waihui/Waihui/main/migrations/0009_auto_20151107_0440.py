# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20151007_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='sku',
            name='roomlink',
            field=models.URLField(default=datetime.datetime(2015, 11, 7, 4, 40, 31, 861673, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sku',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, '\u53ef\u9884\u7ea6'), (1, b'\xe5\xb7\xb2\xe9\xa2\x84\xe7\xba\xa6'), (2, b'\xe8\xa2\xab\xe6\x8b\x92\xe7\xbb\x9d\xe6\x89\x94\xe6\xb1\xa0\xe5\xad\x90\xe7\x9a\x84'), (3, b'\xe5\xbd\xbb\xe5\xba\x95\xe6\xb2\xa1\xe4\xba\xba\xe6\x95\x99'), (4, b'\xe5\xb7\xb2\xe5\xae\x9a'), (5, b'\xe5\xb7\xb2\xe5\xa4\x87\xe8\xaf\xbe'), (6, b'\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbb\xa3\xe8\xaf\x84\xe4\xbb\xb7'), (7, b'\xe5\xb7\xb2\xe5\xbd\xbb\xe5\xba\x95\xe7\xbb\x93\xe6\x9d\x9f ')]),
        ),
    ]
