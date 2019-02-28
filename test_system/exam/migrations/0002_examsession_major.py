# Generated by Django 2.1.7 on 2019-02-26 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='examsession',
            name='major',
            field=models.CharField(blank=True, choices=[('SE', 'Software Engineering'), ('AMI', 'Applied Mathematics and Information Science')], max_length=50, null=True),
        ),
    ]