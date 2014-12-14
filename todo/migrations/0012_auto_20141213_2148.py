# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0011_auto_20141213_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 13, 48, 16, 437090, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
