# Generated by Django 2.1.7 on 2019-03-13 05:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Animal_map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writer', models.CharField(max_length=100)),
                ('Class', models.CharField(blank=True, choices=[('m', 'Mammalia'), ('b', 'Birds'), ('r', 'Reptile'), ('a', 'Amphibia'), ('i', 'Insect')], default='m', help_text='class_Level', max_length=1)),
                ('title', models.CharField(blank=True, max_length=20, null=True)),
                ('Latitude', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('Longitude', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('address', models.CharField(blank=True, choices=[('a', '서울특별시'), ('b', '경기도'), ('c', '강원도'), ('d', '충청북도'), ('e', '충청남도'), ('f', '경상북도'), ('g', '경상남도'), ('h', '전라북도'), ('i', '전라남도'), ('j', '제주도'), ('k', '북한')], default='a', help_text='address_Level', max_length=1)),
                ('content', models.TextField(blank=True, null=True)),
                ('imagefile', models.FileField(upload_to='img')),
                ('soundfile', models.FileField(upload_to='sound')),
                ('file_size_input', models.IntegerField(null=True)),
                ('file_name_input', models.CharField(max_length=30, null=True)),
                ('file_ex_input', models.CharField(max_length=10, null=True)),
                ('duration_input', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('observed_date', models.DateField(default=django.utils.timezone.now, null=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Animal_Sub_file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='subsound')),
                ('label', models.CharField(max_length=30, null=True)),
                ('start_point', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('end_point', models.DecimalField(decimal_places=7, max_digits=10, null=True)),
                ('file_size_input', models.IntegerField(null=True)),
                ('file_name_input', models.CharField(max_length=30, null=True)),
                ('file_ex_input', models.CharField(max_length=10, null=True)),
                ('duration_input', models.IntegerField(null=True)),
                ('Animal_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Animal_map')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('content', models.TextField()),
            ],
        ),
    ]
