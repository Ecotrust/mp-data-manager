# Generated by Django 3.2.12 on 2022-10-05 23:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0047_auto_20220829_2040'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='theme',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='layer',
            name='maxZoom',
            field=models.FloatField(blank=True, default=None, null=True, verbose_name='Maximum zoom'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='minZoom',
            field=models.FloatField(blank=True, default=None, null=True, verbose_name='Minimum zoom'),
        ),
    ]
