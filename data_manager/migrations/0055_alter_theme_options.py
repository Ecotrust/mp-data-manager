# Generated by Django 3.2.12 on 2024-05-17 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0054_auto_20230703_2351'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='theme',
            options={'ordering': ['order']},
        ),
    ]
