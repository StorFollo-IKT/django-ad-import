# Generated by Django 3.1 on 2020-09-18 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad_import', '0003_server_workstation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='target',
            field=models.CharField(choices=[('ad_import.models.workstation', 'Workstation'), ('ad_import.models.server', 'Server'), ('ad_import.models.user', 'User'), ('ad_import.models.group', 'Group')], max_length=200),
        ),
    ]
