# Generated by Django 3.1 on 2020-09-21 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0007_auto_20200922_0028'),
    ]

    operations = [
        migrations.AddField(
            model_name='financialdocument',
            name='child_class',
            field=models.CharField(default='DEFAULT', max_length=50, verbose_name='child_class'),
            preserve_default=False,
        ),
    ]
