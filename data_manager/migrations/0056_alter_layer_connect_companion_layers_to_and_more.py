# Generated by Django 4.2.17 on 2025-01-14 21:13

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0055_alter_theme_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layer',
            name='connect_companion_layers_to',
            field=models.ManyToManyField(blank=True, help_text='Select which main layer(s) you would like to use in conjuction with this companion layer.', to='data_manager.layer'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='sublayers',
            field=models.ManyToManyField(blank=True, to='data_manager.layer'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='vector_color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Vector Fill Color'),
        ),
        migrations.AlterField(
            model_name='layer',
            name='vector_outline_color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Vector Stroke Color'),
        ),
        migrations.AlterField(
            model_name='lookupinfo',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Fill Color'),
        ),
        migrations.AlterField(
            model_name='lookupinfo',
            name='stroke_color',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=[('#FFFFFF', 'white'), ('#888888', 'gray'), ('#000000', 'black'), ('#FF0000', 'red'), ('#FFFF00', 'yellow'), ('#00FF00', 'green'), ('#00FFFF', 'cyan'), ('#0000FF', 'blue'), ('#FF00FF', 'magenta')], verbose_name='Stroke Color'),
        ),
    ]
