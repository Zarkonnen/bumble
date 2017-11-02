# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bumbl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='content',
            field=models.TextField(help_text='Use *** to denote text for markdown.<br>Use {{f:filename}} to get the path of a file.', default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='css',
            field=models.TextField(default='', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=1000, default=''),
            preserve_default=True,
        ),
    ]
