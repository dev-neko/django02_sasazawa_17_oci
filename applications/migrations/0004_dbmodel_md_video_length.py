# Generated by Django 3.2.10 on 2022-06-10 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_rename_md_r_day_dbmodel_md_ts_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbmodel',
            name='md_video_length',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
