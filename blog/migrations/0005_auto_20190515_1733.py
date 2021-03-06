# Generated by Django 2.0.13 on 2019-05-15 08:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190514_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='district',
            old_name='objectid',
            new_name='CTPRVN_CD',
        ),
        migrations.RenameField(
            model_name='district',
            old_name='adm_cd',
            new_name='CTP_ENG_NM',
        ),
        migrations.RenameField(
            model_name='district',
            old_name='adm_cd2',
            new_name='CTP_KOR_NM',
        ),
        migrations.RenameField(
            model_name='district',
            old_name='adm_nm',
            new_name='WKT',
        ),
        migrations.RemoveField(
            model_name='district',
            name='ogc_fid',
        ),
        migrations.RemoveField(
            model_name='district',
            name='wkb_geometry',
        ),
    ]
