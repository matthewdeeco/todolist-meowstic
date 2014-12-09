# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20141209_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 9, 1, 22, 10, 982104, tzinfo=utc), editable=False),
            preserve_default=True,
        ),
    ]
