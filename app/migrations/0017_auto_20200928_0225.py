# Generated by Django 3.1 on 2020-09-27 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20200928_0140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='for_home',
            field=models.BooleanField(default=False, verbose_name='نمایش در پایین صفحه سایت'),
        ),
    ]