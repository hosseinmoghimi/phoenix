# Generated by Django 3.1 on 2020-10-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0032_auto_20201001_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='status',
            field=models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('در جریان', 'در جریان'), ('انجام شده', 'انجام شده'), ('متوقف شده', 'متوقف شده'), ('رد شده', 'رد شده')], default='DEFAULT', max_length=50, verbose_name='status'),
        ),
    ]