# Generated by Django 3.2.12 on 2022-05-25 21:00

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0042_auto_20220525_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='vector_color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Vector Fill Color'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='vector_outline_color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Vector Stroke Color'),
        ),
        migrations.AlterField(
            model_name='lookupinfo',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Fill Color'),
        ),
        migrations.AlterField(
            model_name='lookupinfo',
            name='stroke_color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=18, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Stroke Color'),
        ),
    ]
