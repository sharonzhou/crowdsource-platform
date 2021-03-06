# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-04 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdsourcing', '0075_auto_20160504_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='group_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='revision_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='template',
            name='group_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='template',
            name='revision_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='templateitem',
            name='group_id',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='templateitem',
            name='revision_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('id', 'group_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='template',
            unique_together=set([('id', 'group_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='templateitem',
            unique_together=set([('id', 'group_id')]),
        ),
    ]
