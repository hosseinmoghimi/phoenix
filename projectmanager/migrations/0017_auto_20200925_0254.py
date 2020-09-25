# Generated by Django 3.1 on 2020-09-24 23:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20200923_0246'),
        ('projectmanager', '0016_remove_workunit_employees'),
    ]

    operations = [
        migrations.AddField(
            model_name='managerpage',
            name='documents',
            field=models.ManyToManyField(blank=True, to='app.Document', verbose_name='documents'),
        ),
        migrations.AddField(
            model_name='managerpage',
            name='links',
            field=models.ManyToManyField(blank=True, to='app.Link', verbose_name='links'),
        ),
        migrations.AddField(
            model_name='project',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='projectmanager.project', verbose_name='parent'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('نگهبان', 'نگهبان'), ('مدیر', 'مدیر'), ('فنی', 'فنی'), ('پشتیبان', 'پشتیبان'), ('خدمات', 'خدمات'), ('تایید نشده', 'تایید نشده'), ('سرپرست', 'سرپرست'), ('کارشناس', 'کارشناس'), ('مشاور', 'مشاور'), ('ناظر', 'ناظر'), ('منشی', 'منشی'), ('کارآموز', 'کارآموز'), ('امین اموال', 'امین اموال')], default='تایید نشده', max_length=50, verbose_name='نقش'),
        ),
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Contractor',
                'verbose_name_plural': 'Contractors',
            },
        ),
    ]