# Generated by Django 3.1 on 2020-09-24 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0018_contractor_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contractor',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='contractors',
            field=models.ManyToManyField(blank=True, to='projectmanager.Contractor', verbose_name='contractors'),
        ),
    ]
