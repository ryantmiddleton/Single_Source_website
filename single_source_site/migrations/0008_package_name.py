# Generated by Django 2.2 on 2021-01-14 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('single_source_site', '0007_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='name',
            field=models.CharField(default='No Name', max_length=255),
        ),
    ]