# Generated by Django 2.2.7 on 2019-11-13 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0031_lookupinfo_graphic_scale'),
    ]

    operations = [
        migrations.AddField(
            model_name='lookupinfo',
            name='stroke_color',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Stroke Color'),
        ),
        migrations.AddField(
            model_name='lookupinfo',
            name='stroke_width',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Stroke Width'),
        ),
        migrations.AlterField(
            model_name='lookupinfo',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Fill Color'),
        ),
    ]
