# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150614_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'OrderType',
                'verbose_name_plural': 'OrderTypes',
            },
        ),
        migrations.RenameField(
            model_name='replytosku',
            old_name='to_reply',
            new_name='reply_to',
        ),
        migrations.RenameField(
            model_name='replytosku',
            old_name='from_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='replytosku',
            old_name='from_user',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='buyer',
            name='gender',
            field=models.IntegerField(blank=True, null=True, choices=[(0, b'\xe7\x94\xb7'), (1, b'\xe5\xa5\xb3')]),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='hp',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='pay_method',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='skus',
            field=models.ForeignKey(blank=True, to='main.Sku', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=1, choices=[(0, b'\xe4\xb8\x8d\xe5\x8f\xaf\xe6\x94\xaf\xe4\xbb\x98'), (1, b'\xe6\x9c\xaa\xe6\x94\xaf\xe4\xbb\x98'), (2, b'\xe5\xb7\xb2\xe6\x94\xaf\xe4\xbb\x98'), (3, b'\xe5\xb7\xb2\xe5\xae\x8c\xe6\x88\x90'), (4, b'\xe7\x94\xb3\xe8\xaf\xb7\xe9\x80\x80\xe6\xac\xbe'), (5, b'\xe5\xb7\xb2\xe9\x80\x80\xe6\xac\xbe')]),
        ),
        migrations.AlterField(
            model_name='provider',
            name='fee_rate',
            field=models.FloatField(default=1),
        ),
        migrations.AlterField(
            model_name='provider',
            name='hp',
            field=models.FloatField(default=100),
        ),
        migrations.AlterField(
            model_name='provider',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe9\x9d\x9e\xe6\x95\x99\xe5\xb8\x88'), (1, b'\xe5\xb7\xb2\xe7\x94\xb3\xe8\xaf\xb7'), (2, b'\xe5\xae\x9e\xe4\xb9\xa0'), (3, b'\xe6\xad\xa3\xe5\xbc\x8f')]),
        ),
        migrations.AlterField(
            model_name='sku',
            name='status',
            field=models.IntegerField(default=0, choices=[(0, b'\xe5\x8f\xaf\xe9\xa2\x84\xe7\xba\xa6'), (1, b'\xe5\xb7\xb2\xe9\xa2\x84\xe7\xba\xa6'), (2, b'\xe8\xa2\xab\xe6\x8b\x92\xe7\xbb\x9d\xe6\x89\x94\xe6\xb1\xa0\xe5\xad\x90\xe7\x9a\x84'), (3, b'\xe5\xbd\xbb\xe5\xba\x95\xe6\xb2\xa1\xe4\xba\xba\xe6\x95\x99'), (4, b'\xe5\xb7\xb2\xe5\xae\x9a'), (5, b'\xe5\xb7\xb2\xe5\xa4\x87\xe8\xaf\xbe'), (6, b'\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbb\xa3\xe8\xaf\x84\xe4\xbb\xb7'), (7, b'\xe5\xb7\xb2\xe5\xbd\xbb\xe5\xba\x95\xe7\xbb\x93\xe6\x9d\x9f ')]),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.ForeignKey(default=8, to='main.OrderType'),
            preserve_default=False,
        ),
    ]
