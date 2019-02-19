# Generated by Django 2.1.7 on 2019-02-19 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_answer', '0002_auto_20190215_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_question.TestQuestion'),
        ),
        migrations.AlterField(
            model_name='studentanswer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
