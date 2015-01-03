# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('name', models.SlugField(help_text=b'The set identifier',
                    unique=True, max_length=100)),
                ('add_new_comics', models.BooleanField(default=False,
                    help_text=b'Automatically add new comics to the set')),
                ('hide_empty_comics', models.BooleanField(default=False,
                    help_text=b'Hide comics without matching releases from '
                    b'view')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField()),
                ('last_loaded', models.DateTimeField()),
                ('comics', models.ManyToManyField(to='core.Comic')),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'comics_set',
            },
            bases=(models.Model,),
        ),
    ]
