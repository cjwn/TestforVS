# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20150609_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='provider',
            field=models.ForeignKey(blank=True, to='main.Provider', null=True),
        ),
    ]
