# Generated by Django 4.1.1 on 2022-10-26 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLogsModel',
            fields=[
                ('sys_id', models.AutoField(primary_key=True, serialize=False)),
                ('session_key', models.CharField(blank=True, max_length=1024)),
                ('path', models.CharField(blank=True, max_length=1024)),
                ('method', models.CharField(blank=True, max_length=8)),
                ('data', models.TextField(blank=True, null=True)),
                ('ip_address', models.CharField(blank=True, max_length=45)),
                ('referrer', models.CharField(blank=True, max_length=512, null=True)),
                ('timestamp', models.DateTimeField(blank=True)),
            ],
            options={
                'db_table': 'access_logs',
            },
        ),
    ]
