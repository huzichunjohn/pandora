# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-22 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dnspod', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='domain_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]