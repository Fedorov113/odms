# Generated by Django 3.0.6 on 2020-05-31 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mg_manager', '0007_auto_20200520_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionentry',
            name='schema_collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mg_manager.SchemaCollection'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='collection_entry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries_in_collection', to='mg_manager.CollectionEntry'),
        ),
    ]
