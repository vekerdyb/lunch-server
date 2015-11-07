# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20151101_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='remote_system_id',
            field=models.IntegerField(unique=True, default=1),
            preserve_default=False,
        ),
    ]
