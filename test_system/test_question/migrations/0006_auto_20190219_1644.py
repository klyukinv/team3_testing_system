# Generated by Django 2.1.4 on 2019-02-19 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_question', '0005_auto_20190219_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testquestion',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0, 30), null=True),
        ),
    ]