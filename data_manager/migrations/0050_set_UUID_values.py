# Generated by Django 3.2.12 on 2022-10-07 20:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('data_manager', '0049_auto_20221007_2051'),
    ]

    def gen_uuid(apps, schema_editor):
        AIModel = apps.get_model('data_manager', 'attributeinfo')
        for row in AIModel.objects.all():
            while True:
                row.uuid = uuid.uuid4()
                if not AIModel.objects.filter(uuid=row.uuid).exists():
                    break

            row.save()

        LIModel = apps.get_model('data_manager', 'lookupinfo')
        for row in LIModel.objects.all():
            while True:
                row.uuid = uuid.uuid4()
                if not LIModel.objects.filter(uuid=row.uuid).exists():
                    break

            row.save()
        MDVModel = apps.get_model('data_manager', 'multilayerdimensionvalue')
        for row in MDVModel.objects.all():
            while True:
                row.uuid = uuid.uuid4()
                if not MDVModel.objects.filter(uuid=row.uuid).exists():
                    break

            row.save()

        MDModel = apps.get_model('data_manager', 'multilayerdimension')
        for row in MDModel.objects.all():
            while True:
                row.uuid = uuid.uuid4()
                if not MDModel.objects.filter(uuid=row.uuid).exists():
                    break

            row.save()
        MAModel = apps.get_model('data_manager', 'multilayerassociation')
        for row in MAModel.objects.all():
            while True:
                row.uuid = uuid.uuid4()
                if not MAModel.objects.filter(uuid=row.uuid).exists():
                    break

            row.save()
        TModel = apps.get_model('data_manager', 'theme')
        for row in TModel.objects.all():
            while True:
                row.uuid = uuid.uuid4()
                if not TModel.objects.filter(uuid=row.uuid).exists():
                    break

            row.save()
        LModel = apps.get_model('data_manager', 'layer')
        for row in LModel.objects.all():
            while True:
                row.uuid = uuid.uuid4()
                if not LModel.objects.filter(uuid=row.uuid).exists():
                    break

            row.save()

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]