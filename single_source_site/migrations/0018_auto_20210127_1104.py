# Generated by Django 2.2 on 2021-01-27 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('single_source_site', '0017_auto_20210127_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='quantity_in_order',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity_in_order',
        ),
    ]
