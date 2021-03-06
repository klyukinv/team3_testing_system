# Generated by Django 2.2.1 on 2019-06-01 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('text', models.TextField()),
                ('answ_correct', models.IntegerField()),
                ('answ_option1', models.TextField()),
                ('answ_option2', models.TextField()),
                ('answ_option3', models.TextField()),
                ('answ_option4', models.TextField()),
                ('is_reading', models.BooleanField(default=False)),
            ],
        ),
    ]
