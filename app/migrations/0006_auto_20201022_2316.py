# Generated by Django 2.2.10 on 2020-10-22 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_dataset_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='description',
            field=models.TextField(max_length=200),
        ),
    ]
