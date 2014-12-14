# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_auto_20141213_2138'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='due_on',
            field=models.DateField(blank=True, null=True, default=datetime.date(2014, 12, 13)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 13, 41, 44, 733389, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
