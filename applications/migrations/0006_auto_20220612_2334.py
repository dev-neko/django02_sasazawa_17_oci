# Generated by Django 3.2.10 on 2022-06-12 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0005_dbmodel_md_video_recorded_at_jst'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbmodel',
            name='md_video_length',
        ),
        migrations.RemoveField(
            model_name='dbmodel',
            name='md_video_recorded_at_jst',
        ),
    ]
