# Generated by Django 5.1.1 on 2024-09-16 05:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_soft', '0002_manualreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='manualreport',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=False,
        ),
    ]
