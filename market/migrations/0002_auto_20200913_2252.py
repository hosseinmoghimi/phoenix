# Generated by Django 3.1 on 2020-09-13 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_homeslider_for_home'),
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tag',
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.Tag', verbose_name='برچسب ها'),
        ),
    ]
