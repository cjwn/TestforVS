# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_replytosku_sku'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('noti', models.IntegerField(choices=[(0, b'\xe8\x80\x81\xe5\xb8\x88\xe5\x8f\x91\xe8\xa1\xa8\xe4\xba\x86reply'), (1, b'\xe8\x80\x81\xe5\xb8\x88\xe7\xa1\xae\xe8\xae\xa4\xe4\xba\x86\xe4\xbd\xa0\xe7\x9a\x84\xe8\xaf\xbe\xef\xbc\x8c\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xbc\x80\xe5\xa7\x8b\xe5\xa4\x87\xe8\xaf\xbe'), (2, b'\xe8\x80\x81\xe5\xb8\x88\xe5\xb7\xb2\xe7\xbb\x8f\xe5\xa4\x87\xe8\xaf\xbe\xe5\xae\x8c\xe6\x88\x90\xef\xbc\x81'), (3, b'\xe8\xbf\x98\xe6\x9c\x89\xe5\x8d\x8a\xe4\xb8\xaa\xe5\xb0\x8f\xe6\x97\xb6'), (4, b'\xe5\xbc\x80\xe5\xa7\x8b\xe4\xb8\x8a\xe8\xaf\xbe\xef\xbc\x81(5\xe5\x88\x86\xe9\x92\x9f)'), (5, b'\xe8\x80\x81\xe5\xb8\x88\xe7\xa1\xae\xe8\xae\xa4\xe4\xba\x86\xe4\xbd\xa0\xe7\x9a\x84\xe8\xaf\xbe\xef\xbc\x8c\xe4\xbd\x86\xe6\x98\xaf\xe6\x8d\xa2\xe4\xba\x86\xe8\x80\x81\xe5\xb8\x88'), (6, b'\xe6\x8a\xb1\xe6\xad\x89\xef\xbc\x8c\xe7\x94\xb1\xe4\xba\x8e\xe8\x80\x81\xe5\xb8\x88\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4\xe5\xae\x89\xe6\x8e\x92\xef\xbc\x8c\xe8\xaf\xbe\xe7\xa8\x8b\xe5\x8f\x96\xe6\xb6\x88\xe3\x80\x82\xe9\x80\x80\xe6\xac\xbe\xe5\x88\xb0\xe8\xb4\xa6\xe6\x88\xb7\xe4\xbd\x99\xe9\xa2\x9d'), (7, b'\xe6\x95\x99\xe6\xa1\x88\xe8\xa2\xab\xe4\xbf\xae\xe6\x94\xb9'), (8, b'\xe5\xad\xa6\xe7\x94\x9f\xe9\xa2\x84\xe8\xae\xa2\xe4\xbd\xa0\xe7\x9a\x84\xe8\xaf\xbe\xe5\x95\xa6\xef\xbc\x81\xe8\xaf\xa5\xe5\xa4\x87\xe8\xaf\xbe\xe4\xba\x86\xe8\xaf\xb7\xe7\xa1\xae\xe8\xae\xa4'), (9, b'\xe5\xad\xa6\xe7\x94\x9f\xe5\x8f\x96\xe6\xb6\x88\xe4\xba\x86\xe8\xaf\xbe'), (10, b'\xe5\xad\xa6\xe7\x94\x9f\xe5\x8f\x91\xe8\xa1\xa8\xe4\xba\x86\xe5\x9b\x9e\xe5\xa4\x8d'), (11, b'\xe8\xb6\x85\xe7\xba\xa7\xe9\x80\x9a\xe7\x9f\xa5')])),
                ('note', models.CharField(max_length=200, null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('open_time', models.DateTimeField(null=True, blank=True)),
                ('close_time', models.DateTimeField(null=True, blank=True)),
                ('read', models.IntegerField(choices=[(0, b'unread'), (1, b'readed')])),
                ('reply', models.ForeignKey(blank=True, to='main.ReplyToSku', null=True)),
                ('sku', models.ForeignKey(blank=True, to='main.Sku', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
