# Generated by Django 2.2.4 on 2019-08-21 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_room_avg_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='number',
            field=models.CharField(default='', max_length=30),
        ),
    ]
