# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-05 19:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crowdsourcing', '0077_auto_20160505_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='group_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default=b'Untitled Project', error_messages={b'required': b'Please enter the project name!'}, max_length=256),
        ),
        migrations.AlterField(
            model_name='project',
            name='revision_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 5, 19, 13, 8, 312087, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='group_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='revision_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 5, 19, 13, 19, 895645, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='template',
            name='group_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='revision_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 5, 19, 13, 25, 255031, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='templateitem',
            name='group_id',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='templateitem',
            name='revision_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 5, 19, 13, 52, 982487, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
