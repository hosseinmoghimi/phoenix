# Generated by Django 3.1 on 2020-09-26 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0023_auto_20200925_2152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('managerpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.managerpage')),
                ('date_report', models.DateTimeField(verbose_name='date_report')),
                ('issue_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_for_what', to='projectmanager.managerpage', verbose_name='issue_for')),
            ],
            options={
                'verbose_name': 'Issue',
                'verbose_name_plural': 'Issues',
            },
            bases=('projectmanager.managerpage',),
        ),
    ]