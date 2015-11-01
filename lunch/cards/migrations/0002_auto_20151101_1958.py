# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20151101_1943'),
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='user',
        ),
        migrations.AddField(
            model_name='card',
            name='profile',
            field=models.ForeignKey(to='profiles.Profile', default=1),
            preserve_default=False,
        ),
    ]
