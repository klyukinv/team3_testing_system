# Generated by Django 2.1.7 on 2019-02-25 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import evaluation.models


class Migration(migrations.Migration):

    dependencies = [
        ('speaking_queue', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evaluation', '0004_auto_20190222_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='mark',
            name='level',
            field=models.CharField(choices=[('A1', 'Beginner'), ('A2', 'Elementary'), ('B1', 'Pre-Intermediate'), ('B2', 'Intermediate'), ('C1', 'Upper-Intermediate'), ('C2', 'Advanced')], default=evaluation.models.TestLevel('Beginner'), max_length=29),
        ),
        migrations.AddField(
            model_name='mark',
            name='removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mark',
            name='speaking',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='speaking_queue.TeacherSpeaking'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mark',
            name='speaking_mark',
            field=models.CharField(choices=[('A1m', 'Beginner-'), ('A1p', 'Beginner+'), ('A2m', 'Elementary-'), ('A2p', 'Elementary+'), ('B1m', 'Pre-Intermediate-'), ('B1p', 'Pre-Intermediate+'), ('B2m', 'Intermediate-'), ('B2p', 'Intermediate+'), ('C1m', 'Upper-Intermediate-'), ('C1p', 'Upper-Intermediate+'), ('C2m', 'Advanced-'), ('C2p', 'Advanced+')], default=evaluation.models.SpeakingLevel('Beginner-'), max_length=29),
        ),
        migrations.AddField(
            model_name='mark',
            name='test_level',
            field=models.CharField(choices=[('A1', 'Beginner'), ('A2', 'Elementary'), ('B1', 'Pre-Intermediate'), ('B2', 'Intermediate'), ('C1', 'Upper-Intermediate'), ('C2', 'Advanced')], default=evaluation.models.TestLevel('Beginner'), max_length=29),
        ),
        migrations.AddField(
            model_name='mark',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]