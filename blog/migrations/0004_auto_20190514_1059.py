# Generated by Django 2.0.13 on 2019-05-14 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_district'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animal_map',
            old_name='Class',
            new_name='animalclass',
        ),
    ]
