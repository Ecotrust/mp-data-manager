# Generated by Django 2.2.7 on 2019-11-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0032_auto_20191113_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='show_legend',
            field=models.BooleanField(default=True, help_text='show the legend for this layer if available'),
        ),
    ]
