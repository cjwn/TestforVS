# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_auto_20150621_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.IntegerField(default=0, choices=[(0, b'\xe7\xbd\x91\xe9\xa1\xb5\xe7\xab\xaf'), (1, b'\xe7\xa7\xbb\xe5\x8a\xa8\xe7\xbd\x91\xe9\xa1\xb5\xe7\xab\xaf'), (2, b'IOS\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf'), (3, b'\xe5\xae\x89\xe5\x8d\x93\xe5\xae\xa2\xe6\x88\xb7\xe7\xab\xaf')])),
                ('type', models.IntegerField(choices=[(0, b'\xe7\x99\xbb\xe9\x99\x86'), (1, b'\xe7\x99\xbb\xe5\x87\xba'), (2, b'\xe4\xb8\x8b\xe5\x8d\x95'), (3, b'\xe4\xbf\xae\xe6\x94\xb9'), (4, b'\xe5\x8f\x96\xe6\xb6\x88')])),
                ('character', models.IntegerField(choices=[(0, b'buyer'), (1, b'provider')])),
                ('Dtime', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='ReviewToProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionnaire', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=250, null=True, blank=True)),
                ('score', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(to='main.Buyer')),
                ('provider', models.ForeignKey(to='main.Provider')),
                ('sku', models.OneToOneField(to='main.Sku')),
            ],
            options={
                'verbose_name': 'ReviewTovProvider',
                'verbose_name_plural': 'ReviewTovProviders',
            },
        ),
        migrations.RemoveField(
            model_name='reviewtovprovider',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='reviewtovprovider',
            name='provider',
        ),
        migrations.RemoveField(
            model_name='reviewtovprovider',
            name='sku',
        ),
        migrations.DeleteModel(
            name='ReviewTovProvider',
        ),
    ]
