# Generated by Django 2.1.7 on 2019-03-08 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190308_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal_sub_file',
            name='duration_input',
        ),
        migrations.RemoveField(
            model_name='animal_sub_file',
            name='file_ex_input',
        ),
        migrations.RemoveField(
            model_name='animal_sub_file',
            name='file_name_input',
        ),
        migrations.RemoveField(
            model_name='animal_sub_file',
            name='file_size_input',
        ),
    ]