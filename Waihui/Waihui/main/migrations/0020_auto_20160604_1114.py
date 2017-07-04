# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_auto_20160430_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='avatar',
            field=models.ImageField(default=b'/media/none/a.png', null=True, upload_to=b'provider_avatars/%Y/%m/%d/', blank=True),
        ),
        migrations.AlterField(
            model_name='reviewtobuyer',
            name='sku',
            field=models.ForeignKey(to='main.Sku'),
        ),
    ]
