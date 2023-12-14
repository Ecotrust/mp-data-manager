# Generated by Django 3.2.16 on 2023-07-03 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0052_externalportal'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='password_protected',
            field=models.BooleanField(default=False, help_text='check this if the server requires a password to show layers'),
        ),
    ]
