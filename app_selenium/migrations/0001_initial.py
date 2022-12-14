# Generated by Django 4.1.2 on 2022-10-24 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='proxyListModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=125)),
                ('country', models.CharField(blank=True, max_length=125, null=True)),
                ('link_api', models.CharField(blank=True, max_length=500, null=True)),
                ('data', models.FileField(blank=True, null=True, upload_to='app_selenium/proxylist')),
            ],
            options={
                'verbose_name': 'Proxy List',
            },
        ),
    ]
