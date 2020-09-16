from .apps import APP_NAME
from django.db import models
from django.db.models import Avg, Max, Min
from django.conf import settings
from django.shortcuts import reverse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from django.utils.translation import gettext as _
from io import BytesIO
from .enums import EmployeeEnum,ProfileEnum,OrderStatusEnum
from .constants import *
from app.enums import DegreeLevelEnum,TransactionDirectionEnum, IconsEnum, RegionEnum,AddressTitleEnum
from app.persian import PersianCalendar
from app.repo import ParameterRepo
from app.models import Profile
from app.settings import ADMIN_URL,MEDIA_URL,STATIC_URL
from PIL import Image
import re
import sys
IMAGE_FOLDER=APP_NAME+'/images/'

class ProductUnit(models.Model):
    name=models.CharField(_("واحد فروش"), max_length=50)  
    priority=models.IntegerField(_("ترتیب"),default=1000)

    class Meta:
        verbose_name = _("ProductUnit")
        verbose_name_plural = _("واحد فروش کالا ها")

    def __str__(self):
        return self.name

class Shop(models.Model):
    
    supplier=models.ForeignKey("Supplier", verbose_name=_("فروشگاه"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("واحد فروش"), max_length=50,default='عدد')
    product=models.ForeignKey("Product", verbose_name=_("محصول انتخابی"), on_delete=models.CASCADE)
    price=models.IntegerField(_("قیمت"),default=0)
    available=models.IntegerField(_("تعداد موجودی"),default=DEFAULT_AVAILABLE_PRODUCT_FOR_SHOP)
    time_added=models.DateTimeField(_("تاریخ ثبت پیشنهاد"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("توضیحات"), max_length=500,null=True,blank=True)
    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("کالاهای آماده فروش")

    def __str__(self):
        return self.supplier.title+' (( '+self.product.name+' )) [[ '+(self.unit_name)+' ]]=>  '+str(self.price)
    def product_image(self):
        return str(self.product.image)
    def product_name(self):
        return self.product.name
    def get_absolute_url(self):
        return reverse("market:supplier", kwargs={"supplier_id": self.supplier.pk})
 
class Category(models.Model):
    icon=models.CharField(_("icon"),choices=IconsEnum.choices,default=IconsEnum.important_devices, max_length=50)
    parent=models.ForeignKey("Category", verbose_name=_("دسته بندی بالاتر"),on_delete=models.PROTECT,blank=True,null=True)
    prefix=models.CharField(_("پیش تعریف"), max_length=200,default='',null=True,blank=True)
    name=models.CharField(_("نام دسته"), max_length=50)
    description=models.CharField(_("توضیحات"), max_length=500,default='',null=True,blank=True)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Category/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    rate=models.IntegerField(_("امتیاز"),default=0)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    def image(self):
        return self.image_origin
    
    # def top_products(self):
    #     category_id=self.pk
    #     # products=Product.objects.filter(category_id=category_id)
    #     # for child in Category.objects.filter(parent_id=category_id):
    #     #     products=products | child.top_products(child.id)
    #     # return products[:5]
    #     category_repo=CategoryRepo(user=self.user)
        
    #     products=list(self.list(category_id=category_id).values('id','name'))
    #     for child in category_repo.list(parent_id=category_id):
    #         products+=(self.top_products(child.id))
    #     return products

    def save(self):
        if not self.image_origin:
            super(Category,self).save()             
        elif str(self.image_origin)==str(Category.objects.get(pk=self.id).image_origin):
            super(Category,self).save()
        elif self.image_origin and FORCE_RESIZE_IMAGE:
            # try:
            #     unused_image=Category.objects.get(pk=self.id).image
            #     if unused_image is not None:
            #         input(unused_image)
            #         #unused_image= Image.open(unused_image)
            #         input(unused_image.name)
            #         os.remove(unused_image.name)
            # except:
            #     pass

            #Opening the uploaded image
            image = Image.open(self.image_origin)
       
            output = BytesIO()
           

            #Resize/modify the image
            image = image.resize( (CATEGORY_IMAGE_WIDTH,CATEGORY_IMAGE_HEIGHT),Image.ANTIALIAS )
          
            #after modifications, save it to the output
            image.save(output, format='JPEG', quality=95)
           
            output.seek(0)
           

            #change the imagefield value to be the newley modifed image value
            self.image_origin = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], IMAGE_FOLDER+'Category/image/jpeg', sys.getsizeof(output), None)
            
        super(Category,self).save()
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("دسته بندی ها")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("market:list", kwargs={"parent_id": self.pk})
  
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/category/'+str(self.pk)+'/change/'
    
    def get_breadcrumb_li(self):
        if self is None:
            home='<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':0})+'">خانه</a></li>'        
            return home
        this_category_li='<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':self.pk})+'">'+self.name+'</a></li>'  
        return Category.get_breadcrumb_li(self.parent)+this_category_li

    # def get_breadcrumb_li(self):
    #     if self.parent is None:
    #         home='<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':0})+'">خانه</a></li>'        
    #         return home+'<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':self.id})+'">'+self.name+'</a></li>'  
    #     else:
    #         return self.parent.get_breadcrumb_li()+self.get_breadcrumb_li()
    def get_breadcrumb(self):
        startnav='<nav aria-label="breadcrumb"><ol class="breadcrumb" style="background:none !important;">'
        inside=Category.get_breadcrumb_li(self)         
        endnav='</ol></nav>'
        return startnav+inside+endnav
 
class Brand(models.Model):
    prefix=models.CharField(_("پیش تعریف"), max_length=200,default='',null=True,blank=True)
    name=models.CharField(_("نام برند"), max_length=50)
    description=models.CharField(_("توضیحات"), max_length=500,default='',null=True,blank=True)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Brand/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    rate=models.IntegerField(_("امتیاز"),default=0)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    url=models.CharField(_("آدرس اینترتی"),null=True,blank=True,max_length=100)
    def image(self):
        return MEDIA_URL+str(self.image_origin)
    
    # def top_products(self):
    #     category_id=self.pk
    #     # products=Product.objects.filter(category_id=category_id)
    #     # for child in Category.objects.filter(parent_id=category_id):
    #     #     products=products | child.top_products(child.id)
    #     # return products[:5]
    #     category_repo=CategoryRepo(user=self.user)
        
    #     products=list(self.list(category_id=category_id).values('id','name'))
    #     for child in category_repo.list(parent_id=category_id):
    #         products+=(self.top_products(child.id))
    #     return products

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("برند ها")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse("market:brand", kwargs={"brand_id": self.pk})
        return self.url
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/brand/'+str(self.pk)+'/change/'
    
    def get_breadcrumb_li(self):
        if self is None:
            home='<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':0})+'">خانه</a></li>'        
            return home
        this_category_li='<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':self.pk})+'">'+self.name+'</a></li>'  
        return Category.get_breadcrumb_li(self.parent)+this_category_li

    # def get_breadcrumb_li(self):
    #     if self.parent is None:
    #         home='<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':0})+'">خانه</a></li>'        
    #         return home+'<li class="breadcrumb-item"><a href="'+reverse('market:list',kwargs={'parent_id':self.id})+'">'+self.name+'</a></li>'  
    #     else:
    #         return self.parent.get_breadcrumb_li()+self.get_breadcrumb_li()
    def get_breadcrumb(self):
        startnav='<nav aria-label="breadcrumb"><ol class="breadcrumb" style="background:none !important;">'
        inside=Category.get_breadcrumb_li(self)         
        endnav='</ol></nav>'
        return startnav+inside+endnav

class Employee(models.Model):
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.PROTECT)
    employer_supplier=models.ForeignKey("Supplier", verbose_name=_("supplier"), on_delete=models.CASCADE,null=True,blank=True)
    employer_shipper=models.ForeignKey("Shipper", verbose_name=_("shipper"), on_delete=models.CASCADE,null=True,blank=True)
    
    degree=models.CharField(_("degree"),choices=DegreeLevelEnum.choices,default=DegreeLevelEnum.KARSHENASI, max_length=50)
    major=models.CharField(_("major"), max_length=50)
    def __str__(self):
        return self.profile.name()
    
    def name(self):
        if self.profile is not None:
            return self.profile.name()
        return "پروفایل خالی"
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("کارمندان")
    
    def get_absolute_url(self):
        return reverse('app:profile',kwargs={'profile_id':self.profile.pk})
    def get_edit_url(self):
        if self.profile is not None:
            return self.profile.get_edit_url()

class Accountant(Employee):
    
    class Meta:
        verbose_name = _("Accountant")
        verbose_name_plural = _("حسابداران")

    def get_absolute_url(self):
        return reverse('market:accountant',kwargs={'accountant_id':self.pk})
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/accountant/'+str(self.pk)+'/change/'

class Cashier(Employee):
    
    
    class Meta:
        verbose_name = _("Cashier")
        verbose_name_plural = _("صندوقدار ها")


    def get_absolute_url(self):
        return reverse('market:cashier',kwargs={'cashier_id':self.pk})
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/cashier/'+str(self.pk)+'/change/'

class Manager(Employee):
    
    
    class Meta:
        verbose_name = _("Manager")
        verbose_name_plural = _("مدیر ها")

    
    def get_absolute_url(self):
        return reverse('market:manager',kwargs={'manager_id':self.pk})
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/manager/'+str(self.pk)+'/change/'


class ProductInStock(models.Model):
    adder=models.ForeignKey("Employee", verbose_name=_("ثبت کننده"), on_delete=models.PROTECT)
    ware_house=models.ForeignKey("WareHouse", verbose_name=_("انبار"), on_delete=models.PROTECT)
    product=models.ForeignKey("Product", verbose_name=_("کالا"), on_delete=models.PROTECT)
    quantity=models.IntegerField(_("تعداد"))
    unit_name=models.ForeignKey("ProductUnit", verbose_name=_("واحد"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("تاریخ ثبت"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("توضیحات"), max_length=500,null=True,blank=True)
    class Meta:
        verbose_name = _("ProductInStock")
        verbose_name_plural = _("کالاهای موجود در انبار")

    def __str__(self):
        return f'{self.ware_house.name} => {self.product.name} : {self.quantity} {self.unit_name.name}'

    def get_absolute_url(self):
        return reverse("ProductInStock_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    price=0
    for_home=models.BooleanField(_("نمایش در صفحه خانه"),default=False)
    discount=models.IntegerField(_("درصد تخفیف"),null=True,blank=True)
    is_new=models.BooleanField(_("جدید است؟"),default=False)
    brand=models.ForeignKey("Brand",related_name='brand',null=True,blank=True,on_delete=models.PROTECT)
    category=models.ForeignKey("Category",related_name='products',on_delete=models.PROTECT)
    image=models.ImageField(_("تصویر 1"), upload_to=IMAGE_FOLDER+'Product/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    image2=models.ImageField(_("تصویر 2"), upload_to=IMAGE_FOLDER+'Product/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    image3=models.ImageField(_("تصویر 3"), upload_to=IMAGE_FOLDER+'Product/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    name=models.CharField(_("نام محصول"), max_length=100)
    model_name=models.CharField(_("مدل"),max_length=50,null=True,blank=True)
    barcode=models.CharField(_("بارکد"), max_length=1000,null=True,blank=True)
    rate=models.IntegerField(_("امتیاز"),default=0)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    origin_price=models.IntegerField(_("قیمت بدون تخفیف"),default=0)
    short_description=models.CharField(_("شرح کوتاه"), max_length=500,blank=True,null=True)
    description=models.CharField(_("شرح کامل"), max_length=5000,default='',blank=True,null=True)
    adder=models.ForeignKey("app.Profile",on_delete=models.SET_NULL,null=True,blank=True)
    time_added=models.DateTimeField(_("تاریخ ایجاد"), auto_now=False, auto_now_add=True)
    time_updated=models.DateTimeField(_("تاریخ اصلاح"), auto_now=True, auto_now_add=False)
    thumbnail=models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Product/thumbnail/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    unit_names=models.ManyToManyField("ProductUnit", verbose_name=_("واحد های قابل فروش"))
    related=models.ManyToManyField("Product", verbose_name=_("related"),blank=True)
    comments=models.ManyToManyField("app.Comment", verbose_name=_("نظرات کاربرات"),blank=True)
    tags=models.ManyToManyField("app.Tag", verbose_name=_("برچسب ها"),blank=True)
    def share_mail(self):
        obj={
            'title':self.name+' در فروشگاه '+ParameterRepo().title(),
            'url':self.get_absolute_url(),
            'text':self.name,
            'text_to_view':'share'



        }
        return obj
    def get_image(self):
        if self.image is not None and self.image and len(str(self.image))>0 :
            return MEDIA_URL+str(self.image)
        return STATIC_URL+'dashboard/img/default_avatar.png'
    def get_image2(self):
        if self.image2 is None:
            return self.image
        return MEDIA_URL+str(self.image2)
    def get_image3(self):
        if self.image3 is None:
            return self.image2
        return MEDIA_URL+str(self.image3)
    def get_thumbnail(self):
        if self.thumbnail is None:
            if self.image is None:
                return self.image
            return None
        return self.thumbnail
    def save_temp(self):
        if not self.image:
            super(Product,self).save()             
        elif str(self.image)==str(Product.objects.get(pk=self.id).image):
            super(Product,self).save()
        elif self.image and FORCE_RESIZE_IMAGE:
            if not self.thumbnail:
                self.thumbnail=self.image
            #Opening the uploaded image
            image = Image.open(self.image)
            thumbnail= Image.open(self.thumbnail)
            output = BytesIO()
            output2 = BytesIO()

            #Resize/modify the image
            image = image.resize( (PRODUCT_IMAGE_WIDTH,PRODUCT_IMAGE_HEIGHT),Image.ANTIALIAS )
            thumbnail = thumbnail.resize( (PRODUCT_THUMBNAIL_WIDTH,PRODUCT_THUMBNAIL_HEIGHT),Image.ANTIALIAS )

            #after modifications, save it to the output
            image.save(output, format='JPEG', quality=95)
            thumbnail.save(output2, format='JPEG', quality=95)
            output.seek(0)
            output2.seek(0)

            #change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], IMAGE_FOLDER+'Product/image/jpeg', sys.getsizeof(output), None)
            self.thumbnail = InMemoryUploadedFile(output2,'ImageField', "%s.jpg" %self.thumbnail.name.split('.')[0], IMAGE_FOLDER+'Product/thumbnail/jpeg', sys.getsizeof(output2), None)
            
        super(Product,self).save()
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("کالا ها و محصولات")

    def __str__(self):
        return '%d : %s' % (self.pk, self.name)

    def get_absolute_url(self):
        return reverse("market:product", kwargs={"product_id": self.pk})
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/product/'+str(self.pk)+'/change/'

class ProductSpecification(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    name=models.CharField(_("نام ویژگی"), max_length=50)
    value=models.CharField(_("مقدار ویژگی"), max_length=50)
    class Meta:
        verbose_name = _("ProductSpecification")
        verbose_name_plural = _("ProductSpecifications")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ProductSpecification_detail", kwargs={"id": self.pk})

class ProductComment(models.Model):
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.CASCADE)
    product=models.ForeignKey("Product", verbose_name=_(" محصول"), on_delete=models.CASCADE)
    comment=models.CharField(_('نظر'),max_length=200)
    time_added=models.DateTimeField(_("تاریخ نظر"), auto_now=False, auto_now_add=True)
    def profile_id(self):
        return self.profile.id
    def persian_time_added(self):
        return PersianCalendar().from_gregorian(self.time_added)
    def name(self):
        return self.profile.name()
    def image(self):
        return self.profile.image()
    def __str__(self):
        return self.profile.name()+' '+self.product.name

    class Meta:
        verbose_name = 'ProductComment'
        verbose_name_plural = 'نظر کاربران در مورد محصولات'

class WareHouse(models.Model):
    name=models.CharField(_("نام انبار"), max_length=50)
    address=models.CharField(_("آدرس"), max_length=100)
    agents=models.ManyToManyField("Employee", verbose_name=_("employees"))
    def products_in_stock(self):
        return ProductInStock.objects.filter(ware_house=self)
    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("انبار های کالا")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("market:ware_house", kwargs={"ware_house_id": self.pk})

class Supplier(models.Model):
    region = models.ForeignKey("app.Region", verbose_name=_("region"), on_delete=models.PROTECT)
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.SET_NULL)
    pre_title=models.CharField(_("پیش عنوان"), max_length=50,null=True,blank=True)
    title=models.CharField(_("عنوان"), max_length=50,null=True,blank=True)
    show=models.BooleanField(_("نمایش داده شود؟"),default=False)
    is_verified=models.BooleanField(_("تایید شده؟"),default=False)
    priority=models.IntegerField(_("اولویت"),default=1000)    
    location=models.CharField(_("موقعیت"), max_length=1200,blank=True)
    body=models.CharField(_("متن"), max_length=5000,blank=True)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Supplier/',null=True,blank=True, height_field=None, width_field=None, max_length=None)
    video_title=models.CharField(_("عنوان ویدیو"),blank=True, max_length=100)
    video_link=models.CharField(_("لینک ویدیو"),blank=True, max_length=1000)
    ship_fee=models.IntegerField(_('هزینه ارسال بسته'),default=DEFAULT_SHIPPING_FEE)
    address=models.CharField(_("آدرس"), max_length=100 , null=True,blank=True)
    tel=models.CharField(_("تلفن"), max_length=50 , null=True,blank=True)    
    warehouses=models.ManyToManyField("market.WareHouse", verbose_name=_("warehouses"),blank=True)
    def ware_houses(self):
        return WareHouse.objects.filter(supplier=self)
    def employees(self):
        return Employee.objects.filter(employer_supplier_id=self.pk)    
    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("فروشگاه ها")
    def get_orders_url(self):
        return reverse('market:orders_supplier',kwargs={'supplier_id':self.pk})
    def __str__(self):
        pre_title=  str(self.pre_title)+' ' if self.pre_title else ''
        return pre_title+str(self.title)
    def name(self):
        pre_title=  self.pre_title+' ' if self.pre_title else ''
        return pre_title+self.title
    def mobile(self):
        if self.profile is not None:
            return self.profile.mobile 
        return ""    

    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        else:
            return STATIC_URL+'market/img/default_supplier.png'
    def get_absolute_url(self):
        return reverse('market:supplier',kwargs={'supplier_id':self.pk})


class Shipper(models.Model):
    region = models.ForeignKey("app.Region", verbose_name=_("region"), on_delete=models.PROTECT)
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.SET_NULL)
    title=models.CharField(_("نام موسسه"), max_length=50)
    # show=models.BooleanField(_("نمایش داده شود؟"),default=False)
    is_verified=models.BooleanField(_("تایید شده؟"),default=False)
    priority=models.IntegerField(_("اولویت"),default=1000)
    location=models.CharField(_("موقعیت"), max_length=1200,blank=True)
    body=models.CharField(_("متن"), max_length=5000,blank=True)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Supplier/',null=True,blank=True, height_field=None, width_field=None, max_length=None)
    video_title=models.CharField(_("عنوان ویدیو"),blank=True, max_length=100)
    video_link=models.CharField(_("لینک ویدیو"),blank=True, max_length=1000)
    address=models.CharField(_("آدرس"), max_length=100 , null=True,blank=True)
    tel=models.CharField(_("تلفن"), max_length=50 , null=True,blank=True)
    def employees(self):
        return Employee.objects.filter(employer_supplier_id=self.pk)   
    def mobile(self):
        if self.profile is not None:
            return self.profile.mobile 
        return ""    
    class Meta:
        verbose_name = _("Shipper")
        verbose_name_plural = _("پیک های ارسال کالا")

    def __str__(self):
        return self.title
    def name(self):
        return self.title
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        else:
            return STATIC_URL+'market/img/default_shipper.png'

class Customer(models.Model):
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.SET_NULL)
    favorites=models.ManyToManyField("Product", verbose_name=_("favorites"),blank=True)
    def get_orders_url(self):
        return reverse('market:orders',kwargs={'customer_id':self.pk})
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("مشتریان")
    def __str__(self):
        return self.profile.name()
    

    def save(self):
        self.child_class=ProfileEnum.CUSTOMER
        super(Customer,self).save()
    def get_absolute_url(self):
        return reverse('app:profile',kwargs={'profile_id':self.profile.pk})
    def get_orders_url(self):
        return reverse('market:orders',kwargs={'customer_id':self.pk})
    def get_cart_url(self):
        return reverse('market:cart',kwargs={'customer_id':self.pk})
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/customer/'+str(self.pk)+'/change/'

class Order(models.Model):
    customer=models.ForeignKey("Customer", verbose_name=_("مشتری"), on_delete=models.PROTECT)
    supplier=models.ForeignKey("Supplier", verbose_name=_("فروشگاه"), on_delete=models.PROTECT)
    shipper=models.ForeignKey("Shipper", verbose_name=_("پیک"), on_delete=models.PROTECT,null=True,blank=True)
    
    status=models.CharField(_("وضعیت بسته"), 
        max_length=50,choices=OrderStatusEnum.choices,
        default=OrderStatusEnum.ON_HOLD)
    count_of_packs=models.IntegerField(_("تعداد پاکت"),default=1)
    ship_fee=models.IntegerField(_("هزینه ارسال"))
    address=models.CharField(_("آدرس تحویل"), max_length=200)
    description=models.CharField(_("توضیحات"), max_length=500,null=True,blank=True)
    order_date=models.DateTimeField(_("تاریخ سفارش"), auto_now=False, auto_now_add=True)
    accept_date=models.DateTimeField(_("تاریخ پذیرش"), auto_now=False, auto_now_add=False,null=True,blank=True)
    pack_date=models.DateTimeField(_("تاریخ بسته بندی"), auto_now=False, auto_now_add=False,null=True,blank=True)
    ship_date=models.DateTimeField(_("تاریخ حمل"), auto_now=False, auto_now_add=False,null=True,blank=True)
    deliver_date=models.DateTimeField(_("تاریخ تحویل"), auto_now=False, auto_now_add=False,null=True,blank=True)
    cancel_date=models.DateTimeField(_("تاریخ انصراف"), auto_now=False, auto_now_add=False,null=True,blank=True)
    no_ship=models.BooleanField(_("خودم تحویل میگیرم"),default=False)
    def get_download_url(self):
        return reverse('market:download_order',kwargs={'order_id':self.pk})
    def persian_order_date(self):
        if self.order_date is None:
            return None
        return PersianCalendar().from_gregorian(self.order_date)
    def persian_accept_date(self):
        if self.accept_date is None:
            return None
        return PersianCalendar().from_gregorian(self.accept_date)
    def persian_pack_date(self):   
        if self.pack_date is None:
            return None 
        return PersianCalendar().from_gregorian(self.pack_date)
    def persian_ship_date(self):
        if self.ship_date is None:
            return None
        return PersianCalendar().from_gregorian(self.ship_date)
    def persian_deliver_date(self):
        if self.deliver_date is None:
            return None
        return PersianCalendar().from_gregorian(self.deliver_date)
    def persian_cancel_date(self):
        if self.cancel_date is None:
            return None
        return PersianCalendar().from_gregorian(self.cancel_date)
    

    def supplier_name(self):
        if self.supplier is not None:
            return self.supplier.name
    def shipper_name(self):
        if self.shipper is not None:
            return self.shipper.name
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("سفارش ها")

    def __str__(self):
        return 'سفارش  # '+str(self.pk)+'  '+self.supplier.title+'  => '+self.customer.profile.name()+'   @  '+PersianCalendar().from_gregorian(self.order_date)+'      $ '+str(self.total())
    def total(self):
        if self.no_ship:
            total=self.lines_total()
        else:
            total=self.ship_fee+self.lines_total()        
        return total
    def lines_total(self):
        total=0
        for line in OrderLine.objects.filter(order=self):
            total=total+line.price*line.quantity
        return total
    def get_absolute_url(self):
        return reverse("market:order", kwargs={"order_id": self.pk})

class OrderLine(models.Model):
    order=models.ForeignKey("Order", verbose_name=_("فاکتور"), on_delete=models.CASCADE)
    product=models.ForeignKey("Product", verbose_name=_("محصول"), on_delete=models.PROTECT)
    product_name=models.CharField(_("نام محصول"), max_length=100)
    price=models.IntegerField(_("قیمت"))
    quantity=models.IntegerField(_("تعداد"))
    unit_name=models.CharField(_("واحد"), max_length=50)
    def total(self):
        return self.price*self.quantity
    def product_name(self):
        return self.product.name
    def product_id(self):
        return self.product.id
    def product_image(self):
        return str(self.product.image)
    
    class Meta:
        verbose_name = _("OrderLine")
        verbose_name_plural = _("ریز سفارش ها")

    def __str__(self):
        return ' سفارش '+str(self.order)+' : '+self.product.name+' '+str(self.quantity)+' '+self.unit_name+'*'+str(self.price)+'='+str(self.quantity*self.price)

    def get_absolute_url(self):
        return reverse("OrderLine_detail", kwargs={"pk": self.pk})

class CartLine(models.Model):
    customer=models.ForeignKey("Customer", verbose_name=_("مشتری"), on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField(_("تعداد"),default=1)
    shop=models.ForeignKey("Shop", verbose_name=_("محصول"), on_delete=models.CASCADE,null=True,blank=True)
    time_added=models.DateTimeField(_("تاریخ درخواست"), auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = _("CartLine")
        verbose_name_plural = _("سبد های خرید")
    def persian_time_added(self):
        if self.time_added is None:
            return None 
        return PersianCalendar().from_gregorian(self.time_added) 
    def __str__(self):
        return f'{self.customer.profile.name()} & {self.quantity} # {self.shop.unit_name} {self.shop.product.name} {self.shop.price} $  ({self.shop.supplier.title})'

    def get_absolute_url(self):
        return reverse("CartLine_detail", kwargs={"pk": self.pk})
    def total(self):
        return self.quantity*self.shop.price 

class DeliveryAddress(models.Model):
    customer=models.ForeignKey("Customer", verbose_name=_("مشتری"), on_delete=models.CASCADE)
    title=models.CharField(_("عنوان"), max_length=100,choices=AddressTitleEnum.choices,
        default=AddressTitleEnum.HOME)  
    agent=models.CharField(_("تحویل گیرنده"), max_length=100)  
    street=models.CharField(_("آدرس"), max_length=100)  
    region=models.ForeignKey("app.region",verbose_name=_("region"), on_delete=models.PROTECT)
    
    tel=models.CharField(_("تلفن"), max_length=100)  
    def mobile(self):
        if self.profile is not None:
            return self.customer.mobile 
        return ""    
    class Meta:
        verbose_name = _("DeliveryAddress")
        verbose_name_plural = _("آدرس های تحویل")

    def get_full_address(self):
        return self.title+' تحویل '+self.agent+' تلفن '+self.tel+' ( '+self.city+' - '+self.street+' )'
    def __str__(self):
        return self.title+' '+self.profile.full_name()+' ( '+self.title+' )'
    def get_absolute_url(self):
        return reverse("DeliveryAddress_detail", kwargs={"pk": self.pk})

class ShopRegion(models.Model):
    region=models.CharField(_("نام شهر"), max_length=50,choices=RegionEnum.choices,default=RegionEnum.KHAF)  
    server_address=models.CharField(_("آدرس سرور"), max_length=50)
    class Meta:
        verbose_name = _("ShopRegion")
        verbose_name_plural = _("منطقه های فروش")

    def __str__(self):
        return self.region

    def get_absolute_url(self):
        return reverse("ShopRegion_detail", kwargs={"pk": self.pk})

