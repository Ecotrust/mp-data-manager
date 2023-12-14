# Generated by Django 3.2.16 on 2022-10-19 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0051_auto_20221008_0046'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalPortal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('url', models.URLField(help_text='URL endpoint of the remote Portal')),
            ],
        ),
    ]
