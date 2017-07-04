# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20160424_0823'),
    ]

    operations = [
        migrations.RenameField(
            model_name='provider',
            old_name='avator',
            new_name='avatar',
        ),
    ]
