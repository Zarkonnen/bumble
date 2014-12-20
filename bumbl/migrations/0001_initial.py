# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('commenter', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('ip', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=5000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('title', models.CharField(max_length=1000)),
                ('slug', models.SlugField(blank=True)),
                ('css', models.TextField(blank=True)),
                ('local_css', models.TextField(blank=True)),
                ('total_css', models.TextField(blank=True)),
                ('lead', models.TextField(blank=True)),
                ('content', models.TextField(blank=True, help_text='Use *** to denote text for markdown.<br>Use {{f:filename}} to get the path of a file.')),
                ('section_content', models.TextField(blank=True, help_text='Included in all descendents. Use *** to denote text for markdown.<br>Use {{f:filename}} to get the path of a file.')),
                ('total_section_content', models.TextField(blank=True)),
                ('path', models.TextField(blank=True)),
                ('commentsOn', models.BooleanField(default=True, help_text='Check to allow new comments on a page. Existing comments will be displayed even when this is unchecked.')),
                ('parent', models.ForeignKey(blank=True, null=True, related_name='children', to='bumbl.Entry')),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('f', models.FileField(upload_to='uploads')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('redirect_from', models.CharField(max_length=1000, help_text='Path format: starting slash, no trailing slash. Example: "/foo".')),
                ('redirect_to', models.CharField(max_length=1000, help_text='Path format: starting slash, no trailing slash. Example: "/foo".')),
                ('permanent', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='entries', to='bumbl.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(to='bumbl.Entry'),
            preserve_default=True,
        ),
    ]
