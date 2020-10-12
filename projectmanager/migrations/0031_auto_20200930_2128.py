# Generated by Django 3.1 on 2020-09-30 17:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0030_auto_20200926_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerpage',
            name='app_name',
            field=models.CharField(default='projectmanager', max_length=50, verbose_name='app_name'),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('managerpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.managerpage')),
                ('assign_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projectmanager.employee', verbose_name='کاربر مربوط')),
            ],
            options={
                'verbose_name': 'Assignment',
                'verbose_name_plural': 'Assignments',
            },
            bases=('projectmanager.managerpage',),
        ),
    ]
