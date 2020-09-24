# Generated by Django 3.1 on 2020-09-24 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0010_auto_20200923_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('نگهبان', 'نگهبان'), ('مدیر', 'مدیر'), ('فنی', 'فنی'), ('تایید نشده', 'تایید نشده'), ('حسابدار', 'حسابدار'), ('صندوقدار', 'صندوقدار')], default='تایید نشده', max_length=50, verbose_name='نقش')),
                ('degree', models.CharField(choices=[('دیپلم', 'دیپلم'), ('کاردانی', 'کاردانی'), ('کارشناسی', 'کارشناسی'), ('کارشناسی ارشد', 'کارشناسی ارشد'), ('دکتری', 'دکتری')], default='کارشناسی', max_length=50, verbose_name='مدرک')),
                ('major', models.CharField(blank=True, max_length=50, null=True, verbose_name='رشته تحصیلی')),
                ('introducer', models.CharField(blank=True, max_length=50, null=True, verbose_name='معرف')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='emp', to='app.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('model', models.CharField(max_length=50, verbose_name='model')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='projectmanager/images/Material/thumbnail/', verbose_name='تصویر کوچک')),
                ('image', models.ImageField(blank=True, null=True, upload_to='projectmanager/images/Material/', verbose_name='تصویر 1')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='projectmanager/images/Material/', verbose_name='تصویر 2')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='projectmanager/images/Material/', verbose_name='تصویر 3')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
            },
        ),
        migrations.CreateModel(
            name='MaterialBrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='پیش تعریف')),
                ('name', models.CharField(max_length=50, verbose_name='نام برند')),
                ('description', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='توضیحات')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='projectmanager/images/Brand/', verbose_name='تصویر')),
                ('rate', models.IntegerField(default=0, verbose_name='امتیاز')),
                ('priority', models.IntegerField(default=1000, verbose_name='ترتیب')),
                ('url', models.CharField(blank=True, max_length=100, null=True, verbose_name='آدرس اینترتی')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='MaterialObject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.CharField(blank=True, max_length=200, null=True, verbose_name='serial_no')),
                ('barcode1', models.CharField(blank=True, max_length=200, null=True, verbose_name='barcode1')),
                ('borcode2', models.CharField(blank=True, max_length=200, null=True, verbose_name='barcode2')),
                ('barcode3', models.CharField(blank=True, max_length=200, null=True, verbose_name='barcode3')),
                ('package_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='package_no')),
                ('package_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='package_name')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.material', verbose_name='material')),
            ],
            options={
                'verbose_name': 'MaterialObject',
                'verbose_name_plural': 'MaterialObjects',
            },
        ),
        migrations.CreateModel(
            name='MaterialWareHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='location')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('employees', models.ManyToManyField(blank=True, to='projectmanager.Employee', verbose_name='employees')),
            ],
            options={
                'verbose_name': 'MaterialWareHouse',
                'verbose_name_plural': 'MaterialWareHouses',
            },
        ),
        migrations.CreateModel(
            name='MaterialPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('pack_no', models.CharField(max_length=50, verbose_name='pack_no')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('material_objects', models.ManyToManyField(to='projectmanager.MaterialObject', verbose_name='material_objects')),
            ],
            options={
                'verbose_name': 'MaterialPackage',
                'verbose_name_plural': 'MaterialPackages',
            },
        ),
        migrations.CreateModel(
            name='MaterialLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(max_length=50, verbose_name='priority')),
                ('log_type', models.CharField(max_length=50, verbose_name='log_type')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('material_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='material_object', to='projectmanager.materialobject')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to='app.profile')),
            ],
            options={
                'verbose_name': 'MaterialPackage',
                'verbose_name_plural': 'MaterialPackages',
            },
        ),
        migrations.CreateModel(
            name='MaterialCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='پیش تعریف')),
                ('name', models.CharField(max_length=50, verbose_name='نام دسته')),
                ('description', models.CharField(blank=True, default='', max_length=500, null=True, verbose_name='توضیحات')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='projectmanager/images/Category/', verbose_name='تصویر')),
                ('rate', models.IntegerField(default=0, verbose_name='امتیاز')),
                ('priority', models.IntegerField(default=1000, verbose_name='ترتیب')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='projectmanager.materialcategory', verbose_name='دسته بندی بالاتر')),
            ],
            options={
                'verbose_name': 'MaterialCategory',
                'verbose_name_plural': 'MaterialCategories',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.materialbrand', verbose_name='brand'),
        ),
        migrations.AddField(
            model_name='material',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category', to='projectmanager.materialcategory'),
        ),
    ]