# Generated by Django 4.1.2 on 2022-10-15 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0007_job_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='addr',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='completed',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
