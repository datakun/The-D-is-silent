# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import pytz


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Daybooks',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('user_id', models.CharField(max_length=20)),
                ('date_format', models.CharField(max_length=8)),
                ('date', models.DateTimeField(default=datetime.datetime.now(pytz.timezone('Asia/Seoul')))),
                ('weather', models.TextField(max_length=100)),
                ('title', models.TextField(max_length=100)),
                ('content', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
