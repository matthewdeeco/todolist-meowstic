# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20141209_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='completed_on',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 2, 7, 0, 997968, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
