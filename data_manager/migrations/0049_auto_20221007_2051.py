# Generated by Django 3.2.12 on 2022-10-07 20:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0048_auto_20221005_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='attributeinfo',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='layer',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='lookupinfo',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='multilayerassociation',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='multilayerdimension',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='multilayerdimensionvalue',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='theme',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
