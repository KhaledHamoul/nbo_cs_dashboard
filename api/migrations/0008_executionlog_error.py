# Generated by Django 2.2.10 on 2020-10-25 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_result_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='executionlog',
            name='error',
            field=models.TextField(default=''),
        ),
    ]