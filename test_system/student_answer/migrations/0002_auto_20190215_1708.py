# Generated by Django 2.1.4 on 2019-02-15 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_answer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='started',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='studentanswer',
            name='answer',
            field=models.SmallIntegerField(default=32767),
        ),
    ]
