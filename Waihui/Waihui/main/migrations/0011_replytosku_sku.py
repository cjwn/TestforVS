# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20151115_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='replytosku',
            name='sku',
            field=models.ForeignKey(default=1, to='main.Sku'),
            preserve_default=False,
        ),
    ]
