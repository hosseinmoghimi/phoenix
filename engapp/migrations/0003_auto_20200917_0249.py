# Generated by Django 3.1 on 2020-09-16 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engapp', '0002_auto_20200917_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countdownitem',
            name='image_origin',
            field=models.ImageField(blank=True, null=True, upload_to='engapp/images/CountDownItem/', verbose_name='تصویر  345*970 '),
        ),
    ]
