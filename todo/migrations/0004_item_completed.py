# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_item_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='completed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
