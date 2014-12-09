# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_auto_20141209_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cancelled_on',
            field=models.DateField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 13, 51, 1, 80133, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
