# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_auto_20141209_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cancelled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 9, 3, 49, 476054, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
