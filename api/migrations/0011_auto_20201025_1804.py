# Generated by Django 2.2.10 on 2020-10-25 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20201025_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executionlog',
            name='error_message',
            field=models.TextField(),
        ),
    ]