# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=50)),
                ('brithday', models.DateField()),
                ('time_zone', models.CharField(max_length=50)),
                ('hp', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Buyer',
                'verbose_name_plural': 'Buyers',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chinese_name', models.CharField(max_length=50)),
                ('english_name', models.CharField(max_length=50)),
                ('local_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cny_price', models.FloatField()),
                ('cny_paid', models.FloatField(default=0)),
                ('pay_method', models.CharField(max_length=50, null=True)),
                ('buyer', models.ForeignKey(to='main.Buyer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField()),
                ('content', models.TextField()),
                ('assignment', models.TextField()),
                ('slides', models.TextField()),
                ('materiallinks', models.TextField()),
                ('materialhtml', models.TextField()),
                ('voc', models.TextField()),
                ('sumy', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('copy_from', models.ForeignKey(to='main.Plan')),
            ],
            options={
                'verbose_name': 'Plan',
                'verbose_name_plural': 'Plans',
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'\xe9\x9d\x9e\xe6\x95\x99\xe5\xb8\x88'), (2, b'\xe5\xb7\xb2\xe7\x94\xb3\xe8\xaf\xb7'), (3, b'\xe5\xae\x9e\xe4\xb9\xa0'), (4, b'\xe6\xad\xa3\xe5\xbc\x8f')])),
                ('name', models.CharField(max_length=50)),
                ('weekday_pattern', models.CommaSeparatedIntegerField(max_length=200)),
                ('fee_rate', models.FloatField()),
                ('hp', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
            },
        ),
        migrations.CreateModel(
            name='ReplyToSku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_type', models.IntegerField()),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('to_reply', models.ForeignKey(to='main.ReplyToSku')),
            ],
            options={
                'verbose_name': 'ReplyToSku',
                'verbose_name_plural': 'ReplyToSkus',
            },
        ),
        migrations.CreateModel(
            name='ReviewToBuyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionnaire', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(to='main.Buyer')),
                ('provider', models.ForeignKey(to='main.Provider')),
            ],
            options={
                'verbose_name': 'ReviewToBuyer',
                'verbose_name_plural': 'ReviewToBuyers',
            },
        ),
        migrations.CreateModel(
            name='ReviewTovProvider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('questionnaire', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=50)),
                ('score', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('buyer', models.ForeignKey(to='main.Buyer')),
                ('provider', models.ForeignKey(to='main.Provider')),
            ],
            options={
                'verbose_name': 'ReviewTovProvider',
                'verbose_name_plural': 'ReviewTovProviders',
            },
        ),
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'\xe5\x8f\xaf\xe9\xa2\x84\xe7\xba\xa6'), (2, b'\xe5\xb7\xb2\xe9\xa2\x84\xe7\xba\xa6'), (3, b'\xe8\xa2\xab\xe6\x8b\x92\xe7\xbb\x9d\xe6\x89\x94\xe6\xb1\xa0\xe5\xad\x90\xe7\x9a\x84'), (4, b'\xe5\xbd\xbb\xe5\xba\x95\xe6\xb2\xa1\xe4\xba\xba\xe6\x95\x99'), (5, b'\xe5\xb7\xb2\xe5\xae\x9a'), (6, b'\xe5\xb7\xb2\xe5\xa4\x87\xe8\xaf\xbe'), (7, b'\xe5\xb7\xb2\xe7\xbb\x93\xe6\x9d\x9f\xe4\xbb\xa3\xe8\xaf\x84\xe4\xbb\xb7'), (8, b'\xe5\xb7\xb2\xe5\xbd\xbb\xe5\xba\x95\xe7\xbb\x93\xe6\x9d\x9f ')])),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('provider', models.ForeignKey(to='main.Provider')),
            ],
            options={
                'verbose_name': 'Sku',
                'verbose_name_plural': 'Skus',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('status', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
        ),
        migrations.CreateModel(
            name='TopicCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('background_image', models.URLField()),
            ],
            options={
                'verbose_name': 'TopicCategory',
                'verbose_name_plural': 'TopicCategorys',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cny_balance', models.FloatField(default=0)),
                ('display_currency', models.CharField(default=b'CNY', max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallets',
            },
        ),
        migrations.AddField(
            model_name='topic',
            name='category',
            field=models.ForeignKey(to='main.TopicCategory'),
        ),
        migrations.AddField(
            model_name='topic',
            name='creator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sku',
            name='topic',
            field=models.ForeignKey(to='main.Topic'),
        ),
        migrations.AddField(
            model_name='reviewtovprovider',
            name='sku',
            field=models.OneToOneField(to='main.Sku'),
        ),
        migrations.AddField(
            model_name='reviewtobuyer',
            name='sku',
            field=models.OneToOneField(to='main.Sku'),
        ),
        migrations.AddField(
            model_name='plan',
            name='sku',
            field=models.OneToOneField(null=True, blank=True, to='main.Sku'),
        ),
        migrations.AddField(
            model_name='plan',
            name='topic',
            field=models.ForeignKey(to='main.Topic'),
        ),
        migrations.AddField(
            model_name='order',
            name='provider',
            field=models.ForeignKey(to='main.Provider', null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='skus',
            field=models.ForeignKey(to='main.Sku', null=True),
        ),
        migrations.AddField(
            model_name='buyer',
            name='mother_tongue',
            field=models.ForeignKey(to='main.Language'),
        ),
        migrations.AddField(
            model_name='buyer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
