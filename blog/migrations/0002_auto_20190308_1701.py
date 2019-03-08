# Generated by Django 2.1.7 on 2019-03-08 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
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
        migrations.AlterField(
            model_name='animal_map',
            name='duration_input',
            field=models.DecimalField(decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='animal_sub_file',
            name='Animal_map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Animal_map'),
        ),
        migrations.AlterField(
            model_name='animal_sub_file',
            name='end_point',
            field=models.DecimalField(decimal_places=7, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='animal_sub_file',
            name='start_point',
            field=models.DecimalField(decimal_places=7, max_digits=10, null=True),
        ),
    ]