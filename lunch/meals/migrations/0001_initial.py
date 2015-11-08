# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_profile_full_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('meal_type', models.TextField(choices=[('A', 'A'), ('B', 'B'), ('V', 'Vegetarian')])),
                ('date', models.DateField()),
                ('available', models.BooleanField(default=True)),
                ('profile', models.ForeignKey(to='profiles.Profile')),
            ],
        ),
    ]
