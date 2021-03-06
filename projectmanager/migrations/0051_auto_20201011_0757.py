# Generated by Django 3.1 on 2020-10-11 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0050_managerpage_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialwarehouse',
            name='employees',
        ),
        migrations.AddField(
            model_name='project',
            name='assignments',
            field=models.ManyToManyField(blank=True, to='projectmanager.Assignment', verbose_name='وظیفه ها'),
        ),
        migrations.AlterField(
            model_name='contractor',
            name='icon',
            field=models.CharField(choices=[('place', 'place'), ('construction', 'construction'), ('extension', 'extension'), ('engineering', 'engineering'), ('account_circle', 'account_circle'), ('add_shopping_cart', 'add_shopping_cart'), ('apartment', 'apartment'), ('alarm', 'alarm'), ('attach_file', 'attach_file'), ('attach_money', 'attach_money'), ('backup', 'backup'), ('build', 'build'), ('chat', 'chat'), ('dashboard', 'dashboard'), ('delete', 'delete'), ('description', 'description'), ('face', 'face'), ('favorite', 'favorite'), ('get_app', 'get_app'), ('help_outline', 'help_outline'), ('home', 'home'), ('important_devices', 'important_devices'), ('link', 'link'), ('local_shipping', 'local_shipping'), ('lock', 'lock'), ('mail', 'mail'), ('notification_important', 'notification_important'), ('psychology', 'psychology'), ('publish', 'publish'), ('reply', 'reply'), ('schedule', 'schedule'), ('send', 'send'), ('settings', 'settings'), ('share', 'share'), ('sync', 'sync'), ('vpn_key', 'vpn_key')], default='engineering', max_length=50, verbose_name='آیکون'),
        ),
        migrations.AlterField(
            model_name='managerpage',
            name='icon',
            field=models.CharField(choices=[('place', 'place'), ('construction', 'construction'), ('extension', 'extension'), ('engineering', 'engineering'), ('account_circle', 'account_circle'), ('add_shopping_cart', 'add_shopping_cart'), ('apartment', 'apartment'), ('alarm', 'alarm'), ('attach_file', 'attach_file'), ('attach_money', 'attach_money'), ('backup', 'backup'), ('build', 'build'), ('chat', 'chat'), ('dashboard', 'dashboard'), ('delete', 'delete'), ('description', 'description'), ('face', 'face'), ('favorite', 'favorite'), ('get_app', 'get_app'), ('help_outline', 'help_outline'), ('home', 'home'), ('important_devices', 'important_devices'), ('link', 'link'), ('local_shipping', 'local_shipping'), ('lock', 'lock'), ('mail', 'mail'), ('notification_important', 'notification_important'), ('psychology', 'psychology'), ('publish', 'publish'), ('reply', 'reply'), ('schedule', 'schedule'), ('send', 'send'), ('settings', 'settings'), ('share', 'share'), ('sync', 'sync'), ('vpn_key', 'vpn_key')], default='description', max_length=50, verbose_name='آیکون'),
        ),
    ]
