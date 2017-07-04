# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150610_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='assignment',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='copy_from',
            field=models.ForeignKey(blank=True, to='main.Plan', null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='materialhtml',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='materiallinks',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='slides',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='sumy',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='voc',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='replytosku',
            name='to_reply',
            field=models.ForeignKey(blank=True, to='main.ReplyToSku', null=True),
        ),
        migrations.AlterField(
            model_name='reviewtobuyer',
            name='comment',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reviewtobuyer',
            name='questionnaire',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='reviewtovprovider',
            name='comment',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sku',
            name='buyer',
            field=models.ManyToManyField(to='main.Buyer', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='sku',
            name='topic',
            field=models.ForeignKey(blank=True, to='main.Topic', null=True),
        ),
        migrations.AlterField(
            model_name='topiccategory',
            name='name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
