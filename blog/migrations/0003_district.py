# Generated by Django 2.0.13 on 2019-05-13 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_animal_total_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='district',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ogc_fid', models.IntegerField()),
                ('objectid', models.IntegerField()),
                ('adm_nm', models.TextField(null=True)),
                ('adm_cd', models.TextField(null=True)),
                ('adm_cd2', models.TextField(null=True)),
                ('wkb_geometry', models.TextField(null=True)),
            ],
        ),
    ]
