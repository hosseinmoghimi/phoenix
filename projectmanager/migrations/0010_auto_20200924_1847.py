# Generated by Django 3.1 on 2020-09-24 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0009_auto_20200924_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagelog',
            name='manager_page_id',
            field=models.IntegerField(default=0, verbose_name='page'),
        ),
        migrations.AlterField(
            model_name='pagelog',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectmanager.managerpage', verbose_name='page'),
        ),
    ]
