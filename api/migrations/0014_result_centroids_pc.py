# Generated by Django 2.2.10 on 2020-10-28 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_executionlog_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='centroids_pc',
            field=models.TextField(default=''),
        ),
    ]
