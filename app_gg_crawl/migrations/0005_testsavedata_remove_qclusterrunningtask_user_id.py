# Generated by Django 4.1.2 on 2022-11-23 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_gg_crawl', '0004_alter_testggsearchmodel_key_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSaveData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=125)),
                ('data', models.JSONField()),
            ],
            options={
                'verbose_name': 'Save Data',
            },
        ),
        migrations.RemoveField(
            model_name='qclusterrunningtask',
            name='user_id',
        ),
    ]
