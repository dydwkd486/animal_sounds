# Generated by Django 2.1.7 on 2019-03-08 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20190308_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal_sub_file',
            name='duration_input',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='animal_sub_file',
            name='file_ex_input',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='animal_sub_file',
            name='file_name_input',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='animal_sub_file',
            name='file_size_input',
            field=models.IntegerField(null=True),
        ),
    ]