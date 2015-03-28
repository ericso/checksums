# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='url_params',
            new_name='checksum',
        ),
        migrations.AddField(
            model_name='url',
            name='params',
            field=models.CharField(default={}, max_length=512),
            preserve_default=False,
        ),
    ]
