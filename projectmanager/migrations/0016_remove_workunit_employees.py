# Generated by Django 3.1 on 2020-09-24 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0015_auto_20200925_0025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workunit',
            name='employees',
        ),
    ]
