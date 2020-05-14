# Generated by Django 3.0.3 on 2020-05-06 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mg_manager', '0006_samplesource_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='samplesource',
            name='meta_info',
        ),
        migrations.RemoveField(
            model_name='samplesource',
            name='meta_schema',
        ),
        migrations.AddField(
            model_name='entry',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]