# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_item_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='completed_on',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 1, 19, 56, 888968, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
