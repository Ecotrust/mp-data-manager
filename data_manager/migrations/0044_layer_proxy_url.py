# Generated by Django 3.2.12 on 2022-06-07 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0043_auto_20220525_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='proxy_url',
            field=models.BooleanField(default=False, help_text='proxy layer url through marine planner'),
        ),
    ]
