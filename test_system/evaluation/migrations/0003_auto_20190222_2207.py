# Generated by Django 2.1.7 on 2019-02-22 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0002_auto_20190222_2157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='level',
        ),
        migrations.RemoveField(
            model_name='mark',
            name='removed',
        ),
        migrations.RemoveField(
            model_name='mark',
            name='speaking',
        ),
        migrations.RemoveField(
            model_name='mark',
            name='speaking_mark',
        ),
        migrations.RemoveField(
            model_name='mark',
            name='test_level',
        ),
        migrations.RemoveField(
            model_name='mark',
            name='test_mark',
        ),
    ]
