# Generated by Django 3.1 on 2020-09-15 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200915_0115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpic',
            name='name',
            field=models.CharField(choices=[('سایت', 'سایت'), ('سوالات', 'سوالات'), ('جستجو', 'جستجو'), ('ویدیو', 'ویدیو'), ('درباره ما', 'درباره ما'), ('سربرگ ارتباط با ما', 'سربرگ ارتباط با ما'), ('لوگو', 'لوگو'), ('سربرگ مقاله', 'سربرگ مقاله'), ('سربرگ پروژه', 'سربرگ پروژه'), ('سربرگ پیش فرض برای صفحات', 'سربرگ پیش فرض برای صفحات'), ('سربرگ درباره ما', 'سربرگ درباره ما'), ('سربرگ برچسب', 'سربرگ برچسب')], max_length=50, verbose_name='جای تصویر'),
        ),
    ]