# Generated by Django 3.1 on 2020-10-04 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0035_materialinstock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialrequest',
            name='contractor',
        ),
        migrations.RemoveField(
            model_name='project',
            name='contractors',
        ),
        migrations.AlterField(
            model_name='managerpage',
            name='icon',
            field=models.CharField(choices=[('account_circle', 'account_circle'), ('add_shopping_cart', 'add_shopping_cart'), ('apartment', 'apartment'), ('alarm', 'alarm'), ('attach_file', 'attach_file'), ('attach_money', 'attach_money'), ('backup', 'backup'), ('build', 'build'), ('chat', 'chat'), ('dashboard', 'dashboard'), ('delete', 'delete'), ('description', 'description'), ('face', 'face'), ('favorite', 'favorite'), ('get_app', 'get_app'), ('help_outline', 'help_outline'), ('home', 'home'), ('important_devices', 'important_devices'), ('link', 'link'), ('local_shipping', 'local_shipping'), ('lock', 'lock'), ('mail', 'mail'), ('notification_important', 'notification_important'), ('psychology', 'psychology'), ('publish', 'publish'), ('reply', 'reply'), ('schedule', 'schedule'), ('send', 'send'), ('settings', 'settings'), ('share', 'share'), ('sync', 'sync'), ('vpn_key', 'vpn_key')], default='description', max_length=50, verbose_name='آیکون'),
        ),
        migrations.DeleteModel(
            name='Contractor',
        ),
    ]