# Generated by Django 2.2.10 on 2020-10-25 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_remove_executionlog_error_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='executionlog',
            name='error',
            field=models.TextField(default=''),
        ),
    ]
