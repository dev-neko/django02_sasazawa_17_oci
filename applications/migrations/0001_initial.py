# Generated by Django 3.1.7 on 2021-03-25 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQueryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md_query_name', models.CharField(max_length=50, null=True)),
                ('md_radio_url', models.CharField(max_length=50, null=True)),
                ('md_src_url', models.TextField(null=True)),
                ('md_seller_url', models.TextField(null=True)),
                ('md_radio_e_wday_e_time', models.CharField(max_length=50, null=True)),
                ('md_e_wday', models.CharField(max_length=50, null=True)),
                ('md_e_time', models.CharField(max_length=50, null=True)),
                ('md_analysis_pages_radio', models.CharField(max_length=50, null=True)),
                ('md_analysis_pages_str', models.CharField(max_length=50, null=True)),
                ('md_analysis_pages_end', models.CharField(max_length=50, null=True)),
                ('md_radio_ana_end_spec', models.CharField(max_length=50, null=True)),
                ('md_ana_end_spec', models.CharField(max_length=50, null=True)),
                ('md_auto_ext', models.CharField(max_length=50, null=True)),
                ('md_rate_radio', models.CharField(max_length=50, null=True)),
                ('md_rate', models.CharField(max_length=50, null=True)),
                ('md_exclude_id_radio', models.CharField(max_length=50, null=True)),
                ('md_exclude_id', models.TextField(null=True)),
                ('md_exclude_titledesc_radio', models.CharField(max_length=50, null=True)),
                ('md_exclude_titledesc', models.TextField(null=True)),
            ],
        ),
    ]
