# Generated by Django 3.1 on 2020-09-18 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engapp', '0002_auto_20200918_0219'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'verbose_name': 'Banner', 'verbose_name_plural': 'Banners'},
        ),
        migrations.AlterField(
            model_name='banner',
            name='for_home',
            field=models.BooleanField(default=False, verbose_name='Show on homepage'),
        ),
        migrations.AlterField(
            model_name='countdownitem',
            name='counter',
            field=models.IntegerField(default=100, verbose_name='counter'),
        ),
        migrations.AlterField(
            model_name='countdownitem',
            name='for_home',
            field=models.BooleanField(default=False, verbose_name='Show on homepage'),
        ),
        migrations.AlterField(
            model_name='countdownitem',
            name='image_origin',
            field=models.ImageField(blank=True, null=True, upload_to='engapp/images/CountDownItem/', verbose_name='Image  345*970 '),
        ),
        migrations.AlterField(
            model_name='countdownitem',
            name='priority',
            field=models.IntegerField(default=100, verbose_name='priority'),
        ),
        migrations.AlterField(
            model_name='homeslider',
            name='archive',
            field=models.BooleanField(default=False, verbose_name='archive?'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='name',
            field=models.CharField(choices=[('ABOUT_US_SHORT', 'ABOUT_US_SHORT'), ('ABOUT_US', 'ABOUT_US'), ('MOBILE', 'MOBILE'), ('URL', 'URL'), ('EMAIL', 'EMAIL'), ('FAX', 'FAX'), ('TEL', 'TEL'), ('SINCE', 'SINCE'), ('LOCATION', 'LOCATION'), ('ADDRESS', 'ADDRESS'), ('SLOGAN', 'SLOGAN'), ('ABOUT_US_TITLE', 'ABOUT_US_TITLE'), ('TITLE', 'TITLE'), ('CURRENCY', 'CURRENCY'), ('PRE_TILTE', 'PRE_TILTE'), ('VIDEO_TITLE', 'VIDEO_TITLE'), ('VIDEO_LINK', 'VIDEO_LINK'), ('CONTACT_US', 'CONTACT_US'), ('POSTAL_CODE', 'POSTAL_CODE'), ('TERMS', 'TERMS'), ('OUR_TEAM_TITLE', 'OUR_TEAM_TITLE'), ('OUR_TEAM_LINK', 'OUR_TEAM_LINK'), ('CSRF_FAILURE_MESSAGE', 'CSRF_FAILURE_MESSAGE'), ('THEME_COLOR', 'THEME_COLOR')], max_length=50, verbose_name='Parameter Name'),
        ),
    ]
