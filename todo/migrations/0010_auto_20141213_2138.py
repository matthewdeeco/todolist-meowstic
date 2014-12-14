# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0009_auto_20141209_2151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='completed_on',
            new_name='marked_on',
        ),
        migrations.RemoveField(
            model_name='item',
            name='cancelled_on',
        ),
        migrations.AlterField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 13, 13, 38, 33, 812027, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
