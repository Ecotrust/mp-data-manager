# Generated by Django 4.2.17 on 2025-02-11 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0056_alter_layer_connect_companion_layers_to_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='last_success_status',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
