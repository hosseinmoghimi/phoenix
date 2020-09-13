# Generated by Django 3.1 on 2020-09-13 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50, verbose_name='نام')),
                ('lname', models.CharField(max_length=50, verbose_name='نام خانوادگی')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('subject', models.CharField(max_length=50, verbose_name='عنوان پیام')),
                ('message', models.CharField(max_length=50, verbose_name='متن پیام')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
            ],
            options={
                'verbose_name': 'ContactMessage',
                'verbose_name_plural': 'پیام های ارتباط با ما',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه خانه')),
                ('icon', models.CharField(choices=[('account_circle', 'account_circle'), ('add_shopping_cart', 'add_shopping_cart'), ('alarm', 'alarm'), ('attach_file', 'attach_file'), ('attach_money', 'attach_money'), ('backup', 'backup'), ('build', 'build'), ('chat', 'chat'), ('dashboard', 'dashboard'), ('delete', 'delete'), ('description', 'description'), ('face', 'face'), ('favorite', 'favorite'), ('get_app', 'get_app'), ('help_outline', 'help_outline'), ('home', 'home'), ('important_devices', 'important_devices'), ('link', 'link'), ('local_shipping', 'local_shipping'), ('lock', 'lock'), ('mail', 'mail'), ('notification_important', 'notification_important'), ('psychology', 'psychology'), ('publish', 'publish'), ('reply', 'reply'), ('schedule', 'schedule'), ('send', 'send'), ('settings', 'settings'), ('share', 'share'), ('sync', 'sync'), ('vpn_key', 'vpn_key')], default='help_outline', max_length=50, verbose_name='آیکون')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('dark', 'dark'), ('rose', 'rose')], default='primary', max_length=50, verbose_name='رنگ')),
                ('priority', models.IntegerField(verbose_name='ترتیب')),
                ('question', models.CharField(max_length=200, verbose_name='سوال')),
                ('answer', models.CharField(max_length=5000, verbose_name='پاسخ')),
            ],
            options={
                'verbose_name': 'FAQ',
                'verbose_name_plural': 'پرسش های متداول',
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='app/images/OurService/', verbose_name='تصویر')),
                ('url', models.CharField(blank=True, max_length=2000, null=True, verbose_name='لینک')),
                ('icon_fa', models.CharField(blank=True, max_length=50, null=True, verbose_name='آیکون فونت آسوم')),
                ('icon_material', models.CharField(blank=True, choices=[('account_circle', 'account_circle'), ('add_shopping_cart', 'add_shopping_cart'), ('alarm', 'alarm'), ('attach_file', 'attach_file'), ('attach_money', 'attach_money'), ('backup', 'backup'), ('build', 'build'), ('chat', 'chat'), ('dashboard', 'dashboard'), ('delete', 'delete'), ('description', 'description'), ('face', 'face'), ('favorite', 'favorite'), ('get_app', 'get_app'), ('help_outline', 'help_outline'), ('home', 'home'), ('important_devices', 'important_devices'), ('link', 'link'), ('local_shipping', 'local_shipping'), ('lock', 'lock'), ('mail', 'mail'), ('notification_important', 'notification_important'), ('psychology', 'psychology'), ('publish', 'publish'), ('reply', 'reply'), ('schedule', 'schedule'), ('send', 'send'), ('settings', 'settings'), ('share', 'share'), ('sync', 'sync'), ('vpn_key', 'vpn_key')], max_length=100, null=True, verbose_name='آیکون متریال')),
                ('icon_svg', models.TextField(blank=True, null=True, verbose_name='آیکون svg')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('dark', 'dark'), ('rose', 'rose')], default='primary', max_length=50, verbose_name='رنگ')),
                ('width', models.IntegerField(default=128, verbose_name='عرض')),
                ('height', models.IntegerField(default=128, verbose_name='ارتفاع')),
            ],
            options={
                'verbose_name': 'Icon',
                'verbose_name_plural': 'آیکون ها',
            },
        ),
        migrations.CreateModel(
            name='Jumbotron',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pretitle', models.CharField(blank=True, max_length=500, null=True, verbose_name='پیش عنوان')),
                ('title', models.CharField(blank=True, max_length=500, null=True, verbose_name='عنوان')),
                ('posttitle', models.CharField(blank=True, max_length=500, null=True, verbose_name='پس عنوان')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='شرح کوتاه')),
                ('description', models.TextField(verbose_name='شرح کامل')),
                ('action_text', models.CharField(blank=True, max_length=100, null=True, verbose_name='متن دکمه')),
                ('action_url', models.CharField(blank=True, max_length=2000, null=True, verbose_name='لینک دکمه')),
                ('video_text', models.CharField(blank=True, max_length=100, null=True, verbose_name='متن ویدیو')),
                ('video_url', models.CharField(blank=True, max_length=2000, null=True, verbose_name='لینک ویدیو')),
            ],
            options={
                'verbose_name': 'Jumbotron',
                'verbose_name_plural': 'جامبوترون ها',
            },
        ),
        migrations.CreateModel(
            name='MainPic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('سایت', 'سایت'), ('سوالات', 'سوالات'), ('جستجو', 'جستجو'), ('ویدیو', 'ویدیو'), ('درباره ما', 'درباره ما'), ('سربرگ ارتباط با ما', 'سربرگ ارتباط با ما'), ('لوگو', 'لوگو'), ('سربرگ مقاله', 'سربرگ مقاله'), ('سربرگ پروژه', 'سربرگ پروژه'), ('سربرگ پیش فرض برای صفحات', 'سربرگ پیش فرض برای صفحات'), ('سربرگ درباره ما', 'سربرگ درباره ما')], max_length=50, verbose_name='جای تصویر')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='app/images/MainPic/', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'MainPic',
                'verbose_name_plural': 'تصویر های اصلی سایت',
            },
        ),
        migrations.CreateModel(
            name='MetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه اصلی')),
                ('key', models.CharField(default='name', max_length=50, verbose_name='key name')),
                ('value', models.CharField(default='description', max_length=50, verbose_name='key value')),
                ('content', models.CharField(max_length=2000, verbose_name='content')),
            ],
            options={
                'verbose_name': 'MetaData',
                'verbose_name_plural': 'متا دیتا - کلمات کلیدی سئو',
            },
        ),
        migrations.CreateModel(
            name='OurTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام')),
                ('job', models.CharField(max_length=100, verbose_name='سمت')),
                ('description', models.CharField(max_length=500, verbose_name='توضیحات')),
                ('priority', models.IntegerField(default=1000, verbose_name='ترتیب')),
                ('image_origin', models.ImageField(upload_to='app/images/OurTeam/', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'OurTeam',
                'verbose_name_plural': 'تیم ما',
                'db_table': 'OurTeam',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('درباره ما کوتاه', 'درباره ما کوتاه'), ('درباره ما کامل', 'درباره ما کامل'), ('موبایل', 'موبایل'), ('لینک', 'لینک'), ('ایمیل', 'ایمیل'), ('فکس', 'فکس'), ('تلفن', 'تلفن'), ('موقعیت در گوگل مپ', 'موقعیت در گوگل مپ'), ('آدرس', 'آدرس'), ('شرح کوتاه', 'شرح کوتاه'), ('عنوان درباره ما', 'عنوان درباره ما'), ('عنوان', 'عنوان'), ('واحد پول', 'واحد پول'), ('پیش عنوان', 'پیش عنوان'), ('عنوان ویدیو', 'عنوان ویدیو'), ('لینک ویدیو', 'لینک ویدیو'), ('ارتباط با ما', 'ارتباط با ما'), ('کد پستی', 'کد پستی'), ('قوانین', 'قوانین'), ('عنوان تیم ما', 'عنوان تیم ما'), ('لینک تیم ما', 'لینک تیم ما'), ('پیام درخواست نامعتبر', 'پیام درخواست نامعتبر'), ('رنگ سربرگ کروم در موبایل', 'رنگ سربرگ کروم در موبایل')], max_length=50, verbose_name='نام')),
                ('value', models.CharField(max_length=10000, verbose_name='مقدار')),
            ],
            options={
                'verbose_name': 'Parameter',
                'verbose_name_plural': 'پارامتر ها',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('فعال', 'فعال'), ('غیر فعال', 'غیر فعال')], default='فعال', max_length=50, verbose_name='وضعیت')),
                ('first_name', models.CharField(max_length=200, verbose_name='نام')),
                ('last_name', models.CharField(max_length=200, verbose_name='نام خانوادگی')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='موبایل')),
                ('bio', models.CharField(blank=True, max_length=500, null=True, verbose_name='درباره')),
                ('image_origin', models.ImageField(blank=True, max_length=1200, null=True, upload_to='app/images/Profile/', verbose_name='تصویر')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'پروفایل ها',
            },
        ),
        migrations.CreateModel(
            name='ProfileTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_profile_id', models.IntegerField(verbose_name='از')),
                ('to_profile_id', models.IntegerField(verbose_name='به')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('amount', models.IntegerField(verbose_name='مبلغ')),
                ('cash_type', models.CharField(choices=[('CASH', 'CASH'), ('CHEQUE', 'CHEQUE'), ('CARD', 'CARD')], default='CASH', max_length=50, verbose_name='نوع پرداخت')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='شرح')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='ایجاد شده در ')),
            ],
            options={
                'verbose_name': 'ProfileTransaction',
                'verbose_name_plural': 'تراکنش های کابران',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('خواف', 'خواف'), ('نشتیفان', 'نشتیفان'), ('سنگان', 'سنگان'), ('قاسم آباد', 'قاسم آباد'), ('تایباد', 'تایباد'), ('تربت جام', 'تربت جام'), ('فریمان', 'فریمان'), ('مشهد', 'مشهد'), ('تهران', 'تهران'), ('تربت حیدریه', 'تربت حیدریه')], default='خواف', max_length=50, verbose_name='name')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'منطقه ها',
            },
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(verbose_name='priority')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('subtitle', models.CharField(max_length=50, verbose_name='subtitle')),
                ('description', models.CharField(max_length=500, verbose_name='description')),
                ('date', models.DateTimeField(verbose_name='date')),
            ],
            options={
                'verbose_name': 'Resume',
                'verbose_name_plural': 'رزومه',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه اصلی')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='app/images/OurService/', verbose_name='تصویر')),
                ('url', models.CharField(blank=True, max_length=2000, null=True, verbose_name='لینک')),
                ('icon_fa', models.CharField(blank=True, max_length=50, null=True, verbose_name='آیکون فونت آسوم')),
                ('icon_material', models.CharField(blank=True, choices=[('account_circle', 'account_circle'), ('add_shopping_cart', 'add_shopping_cart'), ('alarm', 'alarm'), ('attach_file', 'attach_file'), ('attach_money', 'attach_money'), ('backup', 'backup'), ('build', 'build'), ('chat', 'chat'), ('dashboard', 'dashboard'), ('delete', 'delete'), ('description', 'description'), ('face', 'face'), ('favorite', 'favorite'), ('get_app', 'get_app'), ('help_outline', 'help_outline'), ('home', 'home'), ('important_devices', 'important_devices'), ('link', 'link'), ('local_shipping', 'local_shipping'), ('lock', 'lock'), ('mail', 'mail'), ('notification_important', 'notification_important'), ('psychology', 'psychology'), ('publish', 'publish'), ('reply', 'reply'), ('schedule', 'schedule'), ('send', 'send'), ('settings', 'settings'), ('share', 'share'), ('sync', 'sync'), ('vpn_key', 'vpn_key')], max_length=100, null=True, verbose_name='آیکون متریال')),
                ('icon_svg', models.TextField(blank=True, null=True, verbose_name='آیکون svg')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('dark', 'dark'), ('rose', 'rose')], default='primary', max_length=50, verbose_name='رنگ')),
                ('width', models.IntegerField(default=128, verbose_name='عرض')),
                ('height', models.IntegerField(default=128, verbose_name='ارتفاع')),
            ],
            options={
                'verbose_name': 'SocialLink',
                'verbose_name_plural': 'شبکه اجتماعی',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('jumbotron_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.jumbotron')),
                ('image_banner', models.ImageField(upload_to='app/images/Banner/', verbose_name='تصویر بنر  345*970 ')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه اصلی')),
                ('archive', models.BooleanField(default=False, verbose_name='بایگانی شود؟')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'بنر های  جشنواره ای',
            },
            bases=('app.jumbotron',),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.icon')),
                ('file', models.FileField(upload_to='app/images/Document', verbose_name='فایل ضمیمه')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'اسناد',
            },
            bases=('app.icon',),
        ),
        migrations.CreateModel(
            name='HomeSlider',
            fields=[
                ('jumbotron_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.jumbotron')),
                ('image_banner', models.ImageField(upload_to='app/images/Banner/', verbose_name='تصویر اسلایدر  1333*2000 ')),
                ('archive', models.BooleanField(default=False, verbose_name='بایگانی شود؟')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('tag_number', models.IntegerField(default=100, verbose_name='عدد برچسب')),
                ('tag_text', models.CharField(blank=True, max_length=100, null=True, verbose_name='متن برچسب')),
            ],
            options={
                'verbose_name': 'HomeSlider',
                'verbose_name_plural': 'اسلایدر های صفحه اصلی',
            },
            bases=('app.jumbotron',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.icon')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه اصلی')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'لینک ها',
            },
            bases=('app.icon',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('jumbotron_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.jumbotron')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه اصلی')),
                ('archive', models.BooleanField(default=False, verbose_name='بایگانی شود؟')),
                ('header_image_origin', models.ImageField(blank=True, null=True, upload_to='app/images/Page/Banner/', verbose_name='تصویر سربرگ  345*970 ')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='app/images/Page/', verbose_name='تصویر بزرگ')),
                ('thumbnail_origin', models.ImageField(blank=True, null=True, upload_to='app/images/Page/thumbnail/', verbose_name='تصویر کوچک')),
                ('priority', models.IntegerField(default=1000, verbose_name='ترتیب')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('title_secondary', models.CharField(blank=True, max_length=200, null=True, verbose_name='عنوان دوم')),
                ('description_secondary', models.CharField(blank=True, max_length=2000, null=True, verbose_name='توضیح دوم')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'صفحات',
            },
            bases=('app.jumbotron',),
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_home', models.BooleanField(default=False, verbose_name='نمایش در صفحه خانه')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='app/images/Testimonial/', verbose_name='تصویر')),
                ('title', models.CharField(max_length=2000, verbose_name='عنوان')),
                ('body', models.CharField(blank=True, max_length=2000, null=True, verbose_name='متن')),
                ('footer', models.CharField(max_length=200, verbose_name='پانوشت')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'گفته های مشتریان',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('image_header', models.ImageField(blank=True, null=True, upload_to='app/images/Tag/', verbose_name='تصویر سربرگ')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('icon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.icon', verbose_name='آیکون')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'برچسب ها',
            },
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Signature',
                'verbose_name_plural': 'امضا ها',
            },
        ),
        migrations.CreateModel(
            name='ResumeCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('تجربه ها', 'تجربه ها'), ('آموزش ها', 'آموزش ها'), ('مهارت ها', 'مهارت ها'), ('علاقه ها', 'علاقه ها'), ('گواهینامه ها', 'گواهینامه ها'), ('جایزه ها', 'جایزه ها'), ('کار های انجام شده', 'کار های انجام شده')], default='آموزش ها', max_length=50, verbose_name='title')),
                ('priority', models.IntegerField(verbose_name='priority')),
                ('our_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ourteam', verbose_name='our_team')),
                ('resumes', models.ManyToManyField(to='app.Resume', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'ResumeCategory',
                'verbose_name_plural': 'دسته بندی رزومه',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.region', verbose_name='region'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ourteam',
            name='resume_categories',
            field=models.ManyToManyField(blank=True, to='app.ResumeCategory', verbose_name='ResumeCategories'),
        ),
        migrations.AddField(
            model_name='ourteam',
            name='social_links',
            field=models.ManyToManyField(blank=True, to='app.SocialLink', verbose_name='social_links'),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('body', models.CharField(blank=True, max_length=500, null=True, verbose_name='توضیحات')),
                ('url', models.CharField(blank=True, max_length=1100, null=True, verbose_name='url')),
                ('seen', models.BooleanField(default=False, verbose_name='دیده شد')),
                ('priority', models.IntegerField(default=1000, verbose_name='اولویت')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('date_seen', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ دیده شده')),
                ('icon', models.CharField(default='notification_important', max_length=50, verbose_name='آیکون')),
                ('color', models.CharField(blank=True, choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('dark', 'dark'), ('rose', 'rose')], default='info', max_length=500, null=True, verbose_name='رنگ')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='پروفایل')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'اعلان ها',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='توسط')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'لایک های کاربران',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='نظر')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='توسط')),
                ('replys', models.ManyToManyField(blank=True, to='app.Comment', verbose_name='پاسخ ها')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'نظرات کاربران',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.page')),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'مقالات',
            },
            bases=('app.page',),
        ),
        migrations.CreateModel(
            name='GalleryPhoto',
            fields=[
                ('banner_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.banner')),
            ],
            options={
                'verbose_name': 'GalleryPhoto',
                'verbose_name_plural': 'تصاویر',
            },
            bases=('app.banner',),
        ),
        migrations.CreateModel(
            name='OurService',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.page')),
                ('icon_fa', models.CharField(blank=True, max_length=50, null=True, verbose_name='آیکون فونت آسوم')),
                ('icon_material', models.CharField(blank=True, choices=[('account_circle', 'account_circle'), ('add_shopping_cart', 'add_shopping_cart'), ('alarm', 'alarm'), ('attach_file', 'attach_file'), ('attach_money', 'attach_money'), ('backup', 'backup'), ('build', 'build'), ('chat', 'chat'), ('dashboard', 'dashboard'), ('delete', 'delete'), ('description', 'description'), ('face', 'face'), ('favorite', 'favorite'), ('get_app', 'get_app'), ('help_outline', 'help_outline'), ('home', 'home'), ('important_devices', 'important_devices'), ('link', 'link'), ('local_shipping', 'local_shipping'), ('lock', 'lock'), ('mail', 'mail'), ('notification_important', 'notification_important'), ('psychology', 'psychology'), ('publish', 'publish'), ('reply', 'reply'), ('schedule', 'schedule'), ('send', 'send'), ('settings', 'settings'), ('share', 'share'), ('sync', 'sync'), ('vpn_key', 'vpn_key')], max_length=100, null=True, verbose_name='آیکون متریال')),
                ('icon_svg', models.TextField(blank=True, null=True, verbose_name='آیکون svg')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('dark', 'dark'), ('rose', 'rose')], default='primary', max_length=50, verbose_name='رنگ')),
                ('width', models.IntegerField(default=128, verbose_name='عرض')),
                ('height', models.IntegerField(default=128, verbose_name='ارتفاع')),
            ],
            options={
                'verbose_name': 'OurService',
                'verbose_name_plural': 'خدمات و سرویس ها',
            },
            bases=('app.page',),
        ),
        migrations.CreateModel(
            name='OurWork',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.page')),
                ('location', models.CharField(blank=True, max_length=500, null=True, verbose_name='موقعیت در نقشه گوگل 400*400')),
            ],
            options={
                'verbose_name': 'OurWork',
                'verbose_name_plural': 'پروژه ها',
            },
            bases=('app.page',),
        ),
        migrations.AddField(
            model_name='resume',
            name='documents',
            field=models.ManyToManyField(blank=True, to='app.Document', verbose_name='documents'),
        ),
        migrations.AddField(
            model_name='resume',
            name='links',
            field=models.ManyToManyField(blank=True, to='app.Link', verbose_name='links'),
        ),
        migrations.CreateModel(
            name='PartialPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pretitle', models.CharField(blank=True, max_length=1000, null=True, verbose_name='پیش عنوان')),
                ('title', models.CharField(blank=True, max_length=1000, null=True, verbose_name='عنوان')),
                ('posttitle', models.CharField(blank=True, max_length=1000, null=True, verbose_name='پس عنوان')),
                ('description', models.TextField(verbose_name='شرح کامل')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='app/images/Blog/Partials/', verbose_name='تصویر بزرگ')),
                ('priority', models.IntegerField(default=1000, verbose_name='ترتیب')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.profile', verbose_name='توسط')),
                ('documents', models.ManyToManyField(blank=True, to='app.Document', verbose_name='سند ها و دانلود ها')),
                ('links', models.ManyToManyField(blank=True, to='app.Link', verbose_name='لینک ها')),
            ],
            options={
                'verbose_name': 'PartialPage',
                'verbose_name_plural': 'صفحات جزئی',
            },
        ),
        migrations.AddField(
            model_name='page',
            name='comments',
            field=models.ManyToManyField(blank=True, to='app.Comment', verbose_name='نظرات'),
        ),
        migrations.AddField(
            model_name='page',
            name='documents',
            field=models.ManyToManyField(blank=True, to='app.Document', verbose_name='سند ها و دانلود ها'),
        ),
        migrations.AddField(
            model_name='page',
            name='likes',
            field=models.ManyToManyField(blank=True, to='app.Like', verbose_name='لایک ها'),
        ),
        migrations.AddField(
            model_name='page',
            name='links',
            field=models.ManyToManyField(blank=True, to='app.Link', verbose_name='لینک ها'),
        ),
        migrations.AddField(
            model_name='page',
            name='meta_datas',
            field=models.ManyToManyField(blank=True, to='app.MetaData', verbose_name='کلمات کلیدی'),
        ),
        migrations.AddField(
            model_name='page',
            name='parts',
            field=models.ManyToManyField(blank=True, to='app.PartialPage', verbose_name='صفحات جزئی'),
        ),
        migrations.AddField(
            model_name='page',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.profile', verbose_name='توسط'),
        ),
        migrations.AddField(
            model_name='page',
            name='relateds',
            field=models.ManyToManyField(blank=True, to='app.Page', verbose_name='صفحات مرتبط'),
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.Tag', verbose_name='برچسب ها'),
        ),
        migrations.AddField(
            model_name='document',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.profile', verbose_name='پروفایل'),
        ),
        migrations.CreateModel(
            name='GalleryAlbum',
            fields=[
                ('banner_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='app.banner')),
                ('photos', models.ManyToManyField(blank=True, to='app.GalleryPhoto', verbose_name='تصویر ها')),
            ],
            options={
                'verbose_name': 'GalleryAlbum',
                'verbose_name_plural': 'آلبوم های تصاویر',
            },
            bases=('app.banner',),
        ),
    ]
