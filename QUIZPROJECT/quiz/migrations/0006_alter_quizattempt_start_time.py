# Generated by Django 5.0.3 on 2024-04-03 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_quizattempt_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizattempt',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
