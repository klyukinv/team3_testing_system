# Generated by Django 2.1.7 on 2019-02-25 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0005_auto_20190225_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mark',
            name='speaking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='speaking_queue.TeacherSpeaking'),
        ),
    ]
