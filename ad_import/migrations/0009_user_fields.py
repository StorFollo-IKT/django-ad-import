# Generated by Django 3.1.8 on 2021-08-13 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ad_import', '0008_sid_bytes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('show_last_logon', 'Can show user last logon')]},
        ),
        migrations.AlterField(
            model_name='user',
            name='manager',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manages',
                                    to='ad_import.user', verbose_name='Leder'),
        ),
    ]
