from django.http import HttpResponse,Http404
import uuid 
from .apps import APP_NAME
from .enums import EmployeeEnum,DegreeLevelEnum,ResumeCategoryEnum,IconsEnum, TransactionDirectionEnum, ColorEnum, ParametersEnum, MainPicEnum, ProfileStatusEnum, RegionEnum, TransactionTypeEnum
from .constants import *
from .persian import PersianCalendar
from .settings import *
from .utils import get_qrcode
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models import Avg, Max, Min,F,Q,Sum
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from io import BytesIO
from datetime import datetime
from PIL import Image
import sys
import os
from tinymce import models as tinymce_models
IMAGE_FOLDER=APP_NAME+'/images/'

class Color(models.Model):
    name=models.CharField(_('نام رنگ'),max_length=50)
    color=models.CharField(_('کد رنگ'),max_length=50)
    class Meta:
        verbose_name = _("Color")
        verbose_name_plural = _("رنگ ها")
        
    def __str__(self):
        return self.name    

class Jumbotron(models.Model):
    pretitle=models.CharField(_("پیش عنوان"), max_length=500,blank=True,null=True)
    title=models.CharField(_("عنوان"), max_length=500,blank=True,null=True)
    posttitle=models.CharField(_("پس عنوان"), max_length=500,blank=True,null=True)
    short_description=tinymce_models.HTMLField(_("شرح کوتاه"),max_length=1000,blank=True,null=True)
    # description=models.TextField(_("شرح کامل"),blank=True,null=True)
    description=tinymce_models.HTMLField(_("شرح کامل"),max_length=2000,null=True,blank=True)
    action_text=models.CharField(_("متن دکمه"), max_length=100,blank=True,null=True)
    action_url=models.CharField(_("لینک دکمه"), max_length=2000,blank=True,null=True)
    video_text=models.CharField(_("متن ویدیو"), max_length=100,blank=True,null=True)
    video_url=models.CharField(_("لینک ویدیو"), max_length=2000,blank=True,null=True)
    
    class Meta:
        verbose_name = _("Jumbotron")
        verbose_name_plural = _("جامبوترون ها")
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.action_url
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/jumbotron/{self.pk}/change/'


class CountDownItem(models.Model):
    image_origin=models.ImageField(_("تصویر  345*970 "), upload_to=IMAGE_FOLDER+'CountDownItem/',null=True,blank=True, height_field=None, width_field=None, max_length=None)
    for_home=models.BooleanField(_("نمایش در صفحه اصلی"),default=False)
    pretitle=models.CharField(_("Pre Title"), max_length=500,blank=True,null=True)
    title=models.CharField(_("Title"), max_length=500,blank=True,null=True)
    counter=models.IntegerField(_("شمارنده"),default=100)
    priority=models.IntegerField(_("ترتیب"),default=100)

    
    class Meta:
        verbose_name = _("CountDownItem")
        verbose_name_plural = _("شمارنده ها")
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.title
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/coundownitem/{self.pk}/change/'



class Banner(Jumbotron):
    image_banner=models.ImageField(_("تصویر بنر  345*970 "), upload_to=IMAGE_FOLDER+'Banner/', height_field=None, width_field=None, max_length=None)
    for_home=models.BooleanField(_("نمایش در صفحه اصلی"),default=False)
    archive=models.BooleanField(_("بایگانی شود؟"),default=False)
    priority=models.IntegerField(_("ترتیب"),default=100)
    
    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("بنر های  جشنواره ای")
    def image(self):
        return MEDIA_URL+str(self.image_banner)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.action_url
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/banner/{self.pk}/change/'



class Page(Jumbotron):
    for_home=models.BooleanField(_("نمایش در صفحه اصلی"),default=False)
    archive=models.BooleanField(_("بایگانی شود؟"),default=False)
    
    
    
    header_image_origin=models.ImageField(_("تصویر سربرگ  345*970 "),blank=True,null=True, upload_to=IMAGE_FOLDER+'Page/Banner/', height_field=None, width_field=None, max_length=None)
    image_origin=models.ImageField(_("تصویر بزرگ"),null=True,blank=True, upload_to=IMAGE_FOLDER+'Page/', height_field=None, width_field=None, max_length=None)
    thumbnail_origin=models.ImageField(_("تصویر کوچک"),null=True,blank=True, upload_to=IMAGE_FOLDER+'Page/thumbnail/', height_field=None, width_field=None, max_length=None)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    profile=models.ForeignKey("Profile",null=True,blank=True, verbose_name=_("توسط"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("تاریخ"), auto_now=False, auto_now_add=True)
    tags=models.ManyToManyField("Tag", verbose_name=_("برچسب ها"),blank=True)
    comments=models.ManyToManyField("Comment", verbose_name=_("نظرات"),blank=True)
    likes=models.ManyToManyField("Like", verbose_name=_("لایک ها"),blank=True)
    relateds=models.ManyToManyField("Page", verbose_name=_("صفحات مرتبط") ,blank=True)
    parts=models.ManyToManyField("PartialPage", verbose_name=_("صفحات جزئی"),blank=True)
    title_secondary=models.CharField(_("عنوان دوم"), max_length=200,null=True,blank=True)
    description_secondary=models.CharField(_("توضیح دوم"), max_length=2000,null=True,blank=True)
    links=models.ManyToManyField("Link", verbose_name=_("لینک ها"),blank=True)
    documents=models.ManyToManyField("Document", verbose_name=_("سند ها و دانلود ها"),blank=True)
    meta_datas=models.ManyToManyField("MetaData", verbose_name=_("کلمات کلیدی"),blank=True)
    count_down_items=models.ManyToManyField("CountDownItem", verbose_name=_("شمارنده ها"),blank=True)
    
    app_name=models.CharField(_('app_name'),default=APP_NAME,max_length=50)
    child_class=models.CharField(_('child_class'),default="page",max_length=50)


    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("صفحات")
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def to_persian_date_tag(self):
        return PersianCalendar().tag(self.date_added)
    def thumbnail(self):
        if self.thumbnail_origin is None:
            return None
        return MEDIA_URL+str(self.thumbnail_origin)
    
    def header_image(self):
        if self.header_image_origin is not None and self.header_image_origin:
            return MEDIA_URL+str(self.header_image_origin)
        else:
            try:
                return str(MainPic.objects.get(name=MainPicEnum.PAGE_HEADER_DEFAULT).image())
            except :
                return None
    
    def image(self):
        if self.image_origin is None:
            return None
        return MEDIA_URL+str(self.image_origin)
    def __str__(self):
        if self.title:
            return self.title
        if self.pk:
            return str(self.pk)
        return '-'

    def get_edit_url(self):
        return f'{ADMIN_URL}{self.app_name}/{self.child_class}/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse(f"{self.app_name}:{self.child_class}", kwargs={f"{self.child_class}_id": self.pk})


class PartialPage(models.Model):
    pretitle=models.CharField(_("پیش عنوان"), max_length=1000,null=True,blank=True)
    title=models.CharField(_("عنوان"), max_length=1000,null=True,blank=True)
    posttitle=models.CharField(_("پس عنوان"), max_length=1000,null=True,blank=True)
    description=models.TextField(_("شرح کامل"))
    image_origin=models.ImageField(_("تصویر بزرگ"),null=True,blank=True, upload_to=IMAGE_FOLDER+'Blog/Partials/', height_field=None, width_field=None, max_length=None)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    profile=models.ForeignKey("Profile",null=True,blank=True, verbose_name=_("توسط"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("تاریخ"), auto_now=False, auto_now_add=True)
    links=models.ManyToManyField("Link", verbose_name=_("لینک ها"),blank=True)
    documents=models.ManyToManyField("Document", verbose_name=_("سند ها و دانلود ها"),blank=True)

    album=models.ForeignKey("GalleryAlbum", verbose_name=_("آلبوم تصاویر"), null=True,blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("PartialPage")
        verbose_name_plural = _("صفحات جزئی")
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def to_persian_date_tag(self):
        return PersianCalendar().tag(self.date_added)
    
    def image(self):
        if self.image_origin is None:
            return None
        return MEDIA_URL+str(self.image_origin)
    def __str__(self):
        return f'{self.pk} : {str(self.title)}'

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/partialpage/{self.pk}/change/'


class Signature(models.Model):
    profile=models.ForeignKey("Profile", verbose_name=_("profile"), on_delete=models.PROTECT)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    description=models.CharField(_("description"), max_length=200)
    status=models.CharField(_("status"), max_length=200)
    class Meta:
        verbose_name = _("Signature")
        verbose_name_plural = _("امضا ها")

    def __str__(self):
        return f'{self.profile.name()} : {self.description} @ {PersianCalendar().from_gregorian(self.date_added)}'


class Tag(models.Model):
    priority=models.IntegerField(_("ترتیب"),default=100)
    image_header=models.ImageField(_("تصویر سربرگ"),null=True,blank=True, upload_to=IMAGE_FOLDER+'Tag/', height_field=None, width_field=None, max_length=None)
    title=models.CharField(_("عنوان"), max_length=50)
    icon=models.ForeignKey("Icon", verbose_name=_("آیکون"),null=True,blank=True, on_delete=models.SET_NULL)
    
    def image(self):
        if self.image_header is None:
            return None
        return MEDIA_URL+str(self.image_header)

    def to_link_tag(self):
        return """
        <a href="{get_absolute_url}" class="leo-farsi tag-cloud-link">
             
                {get_icon_tag}
            
              {title}</a>
          """.format(get_absolute_url=tag.get_absolute_url(),get_icon_tag=tag.icon.get_icon_tag(),title=tag.title)    
          
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("برچسب ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app:tag',kwargs={'tag_id':self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}app/tag/{self.pk}/change/'


class Icon(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)    
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'OurService/', height_field=None,null=True,blank=True, width_field=None, max_length=None)
    icon_fa=models.CharField(_("آیکون فونت آسوم"),max_length=50,null=True,blank=True)
    icon_material=models.CharField(_("آیکون متریال"),choices=IconsEnum.choices,null=True,blank=True, max_length=100)
    icon_svg=models.TextField(_("آیکون svg"),null=True,blank=True)
    color=models.CharField(_("رنگ"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    width=models.IntegerField(_("عرض"),default=128)
    height=models.IntegerField(_("ارتفاع"),default=128)
    def get_icon_tag(self):
        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'
        if self.icon_material is not None and len(self.icon_material)>0:
            return f'<i class="text-{self.color} material-icons">{self.icon_material}</i>'
        if self.icon_fa is not None and len(self.icon_fa)>0:
            return f'<i   style="position:inherit !important;" class="text-{self.color} {self.icon_fa}"></i>'
        if self.icon_svg is not None and len(self.icon_svg)>0:
            return f'<span class="text-{self.color}">{self.icon_svg}</span>'
    def get_tag(self):
        if self.url:
            icon=self.get_icon_tag()
            return f'<a title="{self.title}" href="{self.url}">{icon}</a>'
        else:
            return self.get_icon_tag()
      
    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("آیکون ها")

    def __str__(self):
        return self.title
    
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/icon/{self.pk}/change/'
    def image(self):
        if self.image_origin is None:
            return None
        return MEDIA_URL+str(self.image_origin)
    
    def __unicode__(self):
        return self.title
    # def get_absolute_url(self):
    #     return reverse("OurService_detail", kwargs={"pk": self.pk})


class Link(Icon):
    for_home=models.BooleanField(_("نمایش در پایین صفحه سایت"),default=False)
    for_nav=models.BooleanField(_("نمایش در منوی بالای سایت"),default=False)
    priority=models.IntegerField(_("ترتیب"),default=100)
    profile=models.ForeignKey("Profile", verbose_name=_("profile"), on_delete=models.PROTECT)
    url=models.CharField(_("لینک"), max_length=2000,default="#")    
    
    def get_link_icon_tag(self):
        if self.url:
            icon=self.get_icon_tag()
            return f'<a title="{self.title}" href="{self.url}">{icon}</a>'
        else:
            return self.get_icon_tag()
    
    def to_link_tag(self):
        return """
          <a class="btn  btn-round btn-block btn-{color}" href="{url}">
          <i class="material-icons">{icon}</i>
          {title}</a>
        """.format(color=self.color,icon=self.icon,url=self.url,title=self.title)
    
    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("لینک ها")

    def __str__(self):
        return self.title+('*' if self.for_home else '')

    def get_absolute_url(self):
        return self.url

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/link/{self.pk}/change/'


class HomeSlider(Jumbotron):
    image_banner=models.ImageField(_("تصویر اسلایدر  1333*2000 "), upload_to=IMAGE_FOLDER+'Banner/', height_field=None, width_field=None, max_length=None)
    archive=models.BooleanField(_("بایگانی شود؟"),default=False)
    priority=models.IntegerField(_("ترتیب"),default=100)
    text_color=models.CharField(_("رنگ متن"),default="#fff",max_length=20)
    
    
    tag_number=models.IntegerField(_("عدد برچسب"),default=100)
    tag_text=models.CharField(_("متن برچسب"), max_length=100,blank=True,null=True)
    

    class Meta:
        verbose_name = _("HomeSlider")
        verbose_name_plural = _("اسلایدر های صفحه اصلی")
    def image(self):
        return MEDIA_URL+str(self.image_banner)
    def __str__(self):
        return str(self.priority)

    def get_absolute_url(self):
        return reverse("HomeSlider_detail", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/homeslider/{self.pk}/change/'


class Profile(models.Model):
    region = models.ForeignKey("Region", verbose_name=_("region"), on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,null=True,blank=True
    )
    first_name = models.CharField(_("نام"), max_length=200)
    last_name = models.CharField(_("نام خانوادگی"), max_length=200)
    status = models.CharField(_("وضعیت"), max_length=50,choices=ProfileStatusEnum.choices,default=ProfileStatusEnum.ENABLED)
    mobile = models.CharField(_("موبایل"), max_length=50,null=True,blank=True)
    bio = models.CharField(_("درباره"), max_length=500,null=True,blank=True)
    image_origin = models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Profile/', height_field=None, width_field=None, max_length=1200,blank=True,null=True)
    address=models.CharField(_('آدرس'),max_length=100,null=True,blank=True)
    postal_code=models.CharField(_('کد پستی'),max_length=50,null=True,blank=True)
    def name(self):
        return self.first_name+' '+self.last_name
    def get_my_qrcode(self):
        self.save_qrcode()
        return f'{APP_NAME}/images/Profile/{self.pk}.svg'

    def save_qrcode(self):
        try:
            data={
                'profile_id':self.pk,
                'name':self.name,
                'image':SITE_DOMAIN+self.image(),
            }
            img=get_qrcode(data=data)
            file_name=os.path.join(os.path.join(os.path.join(os.path.join(MEDIA_ROOT,APP_NAME),'images'),'Profile'),str(self.pk)+".svg")
            img.save(file_name)
        except :
            pass
        

    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        else:
            return STATIC_URL+'dashboard/img/default_avatar.png'
    def save(self):  
        
        old_image=None      
        try:
            old_image=Profile.objects.get(pk=self.pk).image_origin
        except:
            pass
        if not self.image_origin :
             super(Profile,self).save()
        elif old_image is not None and str(self.image_origin)==str(Profile.objects.get(pk=self.pk).image_origin):
            super(Profile,self).save()
        elif self.image_origin and FORCE_RESIZE_IMAGE:
            #Opening the uploaded image
            image = Image.open(self.image_origin)       
            output = BytesIO()     
            #Resize/modify the image
            image = image.resize( (PROFILE_IMAGE_WIDTH, PROFILE_IMAGE_HEIGHT), Image.ANTIALIAS )
            
            #after modifications, save it to the output
            image.save(output, format='JPEG', quality=95)
           
            output.seek(0)  
            #change the imagefield value to be the newley modifed image value
            self.image_origin = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image_origin.name.split('.')[0], IMAGE_FOLDER+'Profile/image/jpeg', sys.getsizeof(output), None)
            
        super(Profile,self).save()
        

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("پروفایل ها")

    def __str__(self):
        return f'{self.name()} : {self.user.username if self.user else None}'

    def get_absolute_url(self):
        return reverse("app:profile", kwargs={"profile_id": self.pk})
    def get_transactions_url(self):
        return reverse("app:transactions", kwargs={"profile_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/profile/{self.pk}/change/'


class Region(models.Model):
    name=models.CharField(_("name"), max_length=50,choices=RegionEnum.choices,default=RegionEnum.KHAF)
    priority=models.IntegerField(_("ترتیب"),default=100)
    

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("منطقه ها")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Region_detail", kwargs={"pk": self.pk})


class Notification(models.Model):
    profile=models.ForeignKey("Profile", verbose_name=_("پروفایل"), on_delete=models.CASCADE)
    title=models.CharField(_("عنوان"), max_length=50)
    body=models.CharField(_("توضیحات"), max_length=500,null=True,blank=True)
    url=models.CharField(_("url"), max_length=1100,blank=True,null=True)
    seen=models.BooleanField(_('دیده شد'),default=False)
    priority=models.IntegerField(_("اولویت"),default=1000)
    date_added=models.DateTimeField(_('تاریخ ایجاد'),auto_now_add=True,auto_now=False)
    date_seen=models.DateTimeField(_('تاریخ دیده شده'),auto_now_add=False,auto_now=False,null=True,blank=True)
    icon=models.CharField(_("آیکون"), max_length=50,default='notification_important')
    color=models.CharField(_("رنگ"), choices=ColorEnum.choices,default=ColorEnum.INFO, max_length=500,null=True,blank=True)
    # def send(self,user,channel_name,event_name):
    #     try:
    #           PusherChannelEventRepo(user=user).get(channel_name,event_name).send_message(
            
    #         {
    #             'body':self.body,
    #             'title':self.title,
    #             'color':self.color,
    #             'icon':self.icon,
    #             'link':self.link,
    #             'get_absolute_url':self.get_absolute_url(),
    #         }
            
    #         )
    #     except expression as identifier:
    #         pass
      


    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("اعلان ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app:notification", kwargs={"notification_id": self.pk})


class MetaData(models.Model):    
    for_home=models.BooleanField(_("نمایش در صفحه اصلی"),default=False)
    key=models.CharField(_("key name"), max_length=50,default='name')
    value=models.CharField(_("key value"), max_length=50,default='description')
    content=models.CharField(_("content"), max_length=2000)
    class Meta:
        verbose_name = _("MetaData")
        verbose_name_plural = _("متا دیتا - کلمات کلیدی سئو")

    def __str__(self):
        return ('*** '  if self.for_home else '')+f'{self.key} : {self.value}: {self.content[:20]}'

    def get_absolute_url(self):
        return reverse("MetaData_detail", kwargs={"pk": self.pk})


class MainPic(models.Model):
    name=models.CharField(_("جای تصویر"), max_length=50,choices=MainPicEnum.choices)    
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'MainPic/', height_field=None, width_field=None, max_length=None,null=True,blank=True)

    class Meta:
        verbose_name = _("MainPic")
        verbose_name_plural = _("تصویر های اصلی سایت")
    def image(self):
        if self.image_origin is not None:
            return f'{MEDIA_URL}{str(self.image_origin)}'
        return None
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("MainPic_detail", kwargs={"pk": self.pk})
   
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/mainpic/{self.pk}/change/'


class ContactMessage(models.Model):
    fname=models.CharField(_("نام"), max_length=50)
    lname=models.CharField(_("نام خانوادگی"), max_length=50)
    email=models.EmailField(_("ایمیل"), max_length=254)
    subject=models.CharField(_("عنوان پیام"), max_length=50)
    message=models.CharField(_("متن پیام"), max_length=50)
    date_added=models.DateTimeField(_("افزوده شده در"), auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = _("ContactMessage")
        verbose_name_plural = _("پیام های ارتباط با ما")

    def __str__(self):
        return self.email+"   @  "+PersianCalendar().from_gregorian(self.date_added)

    def get_absolute_url(self):
        return reverse("ContactMessage_detail", kwargs={"pk": self.pk})


class Parameter(models.Model):
    name=models.CharField(_("نام"), max_length=50,choices=ParametersEnum.choices)
    value=models.CharField(_("مقدار"), max_length=10000)
    

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("پارامتر ها")

    def __str__(self):
        return f'{self.name} : {self.value}'

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/change/'


class FAQ(models.Model):
    for_home=models.BooleanField(_("نمایش در صفحه خانه"),default=False)
    icon=models.CharField(_("آیکون"),choices=IconsEnum.choices,default=IconsEnum.help_outline, max_length=50)
    color=models.CharField(_("رنگ"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    priority=models.IntegerField(_("ترتیب"))
    question=models.CharField(_("سوال"), max_length=200)
    answer=models.CharField(_("پاسخ"), max_length=5000)
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("پرسش های متداول")

    def __str__(self):
        return self.question

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/faq/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse("app:faq")


class Blog(Page):

    def save(self):
        self.child_class='blog'
        self.app_name=APP_NAME
        super(Blog,self).save()

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("مقالات")
   
    def __str__(self):
        return self.title

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/blog/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse("app:blog", kwargs={"blog_id": self.pk})


class Technology(Page):

    def save(self):
        self.child_class='blog'
        self.app_name=APP_NAME
        super(Technology,self).save()

    
    class Meta:
        verbose_name = _("Technology")
        verbose_name_plural = _("تکنولوژی")
   
    def __str__(self):
        if self.title:
            return self.title
        return str(self.priority)
        

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/technology/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse("app:technology", kwargs={"technology_id": self.pk})


class Comment(models.Model):
    profile=models.ForeignKey("Profile",null=True,blank=True, verbose_name=_("توسط"), on_delete=models.CASCADE)
    text=models.TextField(_("نظر"))
    date_added=models.DateTimeField(_("تاریخ"), auto_now=False, auto_now_add=True)
    replys=models.ManyToManyField("Comment", verbose_name=_("پاسخ ها"),blank=True)
    
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("نظرات کاربران")
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def __str__(self):
        name='' if self.profile is None else self.profile.name()
        return f'{name} @ {self.text}'

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/blog/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse("app:blog", kwargs={"blog_id": self.pk})
    def profile_name(self):
        return self.profile.name()
    def profile_image(self):
        return self.profile.image()
    def profile_id(self):
        return self.profile.pk
    def persian_date_added_tag(self):
        value=self.date_added
        a=PersianCalendar().from_gregorian(value)        
        return f'<a href="#" title="{value.strftime("%Y/%m/%d %H:%M:%S") }">{str(a)}</a>'


class Like(models.Model):
    profile=models.ForeignKey("Profile",null=True,blank=True, verbose_name=_("توسط"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("تاریخ"), auto_now=False, auto_now_add=True)
    
    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("لایک های کاربران")
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def __str__(self):
        name='' if self.profile is None else self.profile.name()
        return f'{name} @ {self.persian_date_added()}'


class OurWorkCategory(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    priority=models.IntegerField(_("ترتیب"),default=100)
    image_header=models.ImageField(_("تصویر سربرگ"),null=True,blank=True, upload_to=IMAGE_FOLDER+'OurWorkCategory/', height_field=None, width_field=None, max_length=None)
     
    def image(self):
        if self.image_header is None:
            return None
        return MEDIA_URL+str(self.image_header)

    def to_link_tag(self):
        return """
        <a href="{get_absolute_url}" class="leo-farsi tag-cloud-link">
             
                {get_icon_tag}
            
              {title}</a>
          """.format(get_absolute_url=tag.get_absolute_url(),get_icon_tag=tag.icon.get_icon_tag(),title=tag.title)    
          
    class Meta:
        verbose_name = _("دسته بندی  پروژه")
        verbose_name_plural = _("دسته بندی  پروژه ها")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app:our_works_by_category',kwargs={'category_id':self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}app/ourworkcategory/{self.pk}/change/'


class OurWork(Page):

    def save(self):
        self.child_class='blog'
        self.app_name=APP_NAME
        super(OurWork,self).save()
    category=models.ForeignKey("OurWorkCategory",null=True,blank=True, verbose_name=_("دسته بندی"), on_delete=models.SET_NULL)
    
    location=models.CharField(_('موقعیت در نقشه گوگل 400*400'),max_length=500,null=True,blank=True)    
    
    class Meta:
        verbose_name = _("OurWork")
        verbose_name_plural = _("پروژه ها")
    
    def __str__(self):
        return self.title

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/ourwork/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse("app:our_work", kwargs={"our_work_id": self.pk})


class Testimonial(models.Model):
    for_home=models.BooleanField(_("نمایش در صفحه خانه"),default=False)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Testimonial/',null=True,blank=True, height_field=None, width_field=None, max_length=None)
    title=models.CharField(_("عنوان"), max_length=2000)
    body=models.CharField(_("متن"), max_length=2000,null=True,blank=True)
    footer=models.CharField(_("پانوشت"), max_length=200)
    priority=models.IntegerField(_("ترتیب"),default=100)
    profile=models.ForeignKey("Profile", null=True,blank=True,verbose_name=_("profile"), on_delete=models.PROTECT)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("گفته های مشتریان")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Testimonial_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/testimonial/{self.pk}/change/'


class OurService(Page):
    icon_fa=models.CharField(_("آیکون فونت آسوم"),max_length=50,null=True,blank=True)
    icon_material=models.CharField(_("آیکون متریال"),choices=IconsEnum.choices,null=True,blank=True, max_length=100)
    icon_svg=models.TextField(_("آیکون svg"),null=True,blank=True)
    color=models.CharField(_("رنگ"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    width=models.IntegerField(_("عرض"),default=128)
    height=models.IntegerField(_("ارتفاع"),default=128)
    

    def save(self):
        self.child_class='blog'
        self.app_name=APP_NAME
        super(OurService,self).save()
    
    def get_icon_tag(self):
        if self.thumbnail_origin is not None and self.thumbnail_origin:
            return f'<img src="{MEDIA_URL}{str(self.thumbnail_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'
        if self.icon_material is not None and len(self.icon_material)>0:
            return f'<i class="text-{self.color} material-icons">{self.icon_material}</i>'
        if self.icon_fa is not None and len(self.icon_fa)>0:
            return f'<span class="text-{self.color} {self.icon_fa}"></span>'
        if self.icon_svg is not None and len(self.icon_svg)>0:
            return f'<span class="text-{self.color}">{self.icon_svg}</span>'
    def get_tag(self):
        icon=self.get_icon_tag()
        return f'<a title="{self.title}" href="{self.get_absolute_url()}">{icon}</a>'
      
    
    class Meta:
        verbose_name = _("OurService")
        verbose_name_plural = _("خدمات و سرویس ها")

    def __str__(self):
        return self.title
    
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/ourservice/{self.pk}/change/'


    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("app:page", kwargs={"page_id": self.pk})




class SocialLink(models.Model):
    for_home=models.BooleanField(_("نمایش در صفحه اصلی"),default=False)
    priority=models.IntegerField(_("ترتیب"),default=100)
    
    title=models.CharField(_("عنوان"), max_length=50)    
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'OurService/', height_field=None,null=True,blank=True, width_field=None, max_length=None)
    url=models.CharField(_("لینک"), max_length=2000,null=True,blank=True)    
    icon_fa=models.CharField(_("آیکون فونت آسوم"),max_length=50,null=True,blank=True)
    icon_material=models.CharField(_("آیکون متریال"),choices=IconsEnum.choices,null=True,blank=True, max_length=100)
    icon_svg=models.TextField(_("آیکون svg"),null=True,blank=True)
    color=models.CharField(_("رنگ"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    width=models.IntegerField(_("عرض"),default=128)
    height=models.IntegerField(_("ارتفاع"),default=128)
    def get_icon_tag(self):
        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'
        if self.icon_material is not None and len(self.icon_material)>0:
            return f'<i class="text-{self.color} material-icons">{self.icon_material}</i>'
        if self.icon_fa is not None and len(self.icon_fa)>0:
            return f'<span class="text-{self.color} {self.icon_fa}"></span>'
        if self.icon_svg is not None and len(self.icon_svg)>0:
            return f'<span class="text-{self.color}">{self.icon_svg}</span>'
    def get_tag(self):
        if self.url:
            icon=self.get_icon_tag()
            return f'<a title="{self.title}" href="{self.url}">{icon}</a>'
        else:
            return self.get_icon_tag()
   
   
    class Meta:
        verbose_name = _("SocialLink")
        verbose_name_plural = _("شبکه اجتماعی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.link


class OurTeam(models.Model):
    name=models.CharField(_("نام"), max_length=100)
    job=models.CharField(_("سمت"), max_length=100)
    description=models.CharField(_("توضیحات"), max_length=500)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'OurTeam/', height_field=None, width_field=None, max_length=None)
    social_links=models.ManyToManyField("SocialLink", verbose_name=_("social_links"),blank=True)
    resume_categories=models.ManyToManyField("ResumeCategory", verbose_name=_("ResumeCategories"),blank=True)
    header_image_origin=models.ImageField(_("تصویر سربرگ"),null=True,blank=True, upload_to=IMAGE_FOLDER+'OurTeam/Header/', height_field=None, width_field=None, max_length=None)
    
    def __str__(self):
        return self.name
    def get_resume_url(self):
        return reverse('app:resume',kwargs={'our_team_id':self.pk})
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        else:
            return STATIC_URL+'dashboard/img/default_avatar.png'
    def header_image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.header_image_origin)
        else:
            return ''
    
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/ourteam/{self.pk}/change/'
    def get_absolute_url(self):
        return reverse('app:our_team',kwargs={'our_team_id':self.pk})

    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'OurTeam'
        managed = True
        verbose_name = 'OurTeam'
        verbose_name_plural = 'تیم ما'


class GalleryAlbum(Jumbotron):
    image_origin=models.ImageField(_("Big Image 345*970 "), upload_to=IMAGE_FOLDER+'Gallery/Album/',null=True,blank=True, height_field=None, width_field=None, max_length=None)
    for_home=models.BooleanField(_("Show on homepage"),default=False)
    archive=models.BooleanField(_("Archive?"),default=False)
    priority=models.IntegerField(_("Priority"),default=100)
    thumbnail_origin=models.ImageField(_("Thumbnail Image"), upload_to=IMAGE_FOLDER+'Gallery/Album/Thumbnail/',null=True,blank=True, height_field=None, width_field=None, max_length=None)
    
    photos=models.ManyToManyField("GalleryPhoto", verbose_name=_("Photos"),blank=True)
    def get_tag(self):
        s= """<div class="row leo-rtl mb-3">"""
        for pic in self.photos.all():
            s+=f"""<div class="col-lg-3">
            <a target="_blank" href="{pic.image()}"><img src="{pic.image()}" width="100%"></a>
            </div>"""
        s+="</div>"
        return s
    def image(self):
        return MEDIA_URL+str(self.image_origin)
    def thumbnail(self):
        return MEDIA_URL+str(self.thumbnail_origin)
    
    class Meta:
        verbose_name = _("GalleryAlbum")
        verbose_name_plural = _("آلبوم های تصاویر")

    def __str__(self):
        return self.title
    
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/galleryalbum/{self.pk}/change/'
   
   
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("OurService_detail", kwargs={"pk": self.pk})


class GalleryPhoto(Jumbotron):
    
    image_origin=models.ImageField(_("Big Image 345*970 "), upload_to=IMAGE_FOLDER+'Gallery/Photo/', height_field=None, width_field=None, max_length=None)
    for_home=models.BooleanField(_("Show on homepage"),default=False)
    archive=models.BooleanField(_("Archive?"),default=False)
    priority=models.IntegerField(_("Priority"),default=100)    
    thumbnail_origin=models.ImageField(_("Thumbnail Image"), upload_to=IMAGE_FOLDER+'Gallery/Photo/Thumbnail/',null=True,blank=True, height_field=None, width_field=None, max_length=None)
    
    def image(self):
        return MEDIA_URL+str(self.image_origin)
    def thumbnail(self):
        return MEDIA_URL+str(self.thumbnail_origin)

    class Meta:
        verbose_name = _("GalleryPhoto")
        verbose_name_plural = _("تصاویر")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app:home")
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/galleryphoto/{self.pk}/change/'
    


class ProfileTransaction(models.Model):
    from_profile_id=models.IntegerField(_('از'))
    to_profile_id=models.IntegerField(_('به'))
    title=models.CharField(_("عنوان"), max_length=50)
    amount=models.IntegerField(_("مبلغ"))
    cash_type=models.CharField(_("نوع پرداخت"),choices=TransactionTypeEnum.choices,default=TransactionTypeEnum.CASH, max_length=50)
    description=models.CharField(_("شرح"), max_length=50,null=True,blank=True)
    date_added=models.DateTimeField(_("ایجاد شده در "), auto_now=False, auto_now_add=True)
    def from_profile(self):
        try:
            return Profile.objects.get(pk=self.from_profile_id)
        except:
            return None
    def to_profile(self):
        try:
            return Profile.objects.get(pk=self.to_profile_id)
        except:
            return None
    class Meta:
        verbose_name = _("ProfileTransaction")
        verbose_name_plural = _("تراکنش های کابران")
    def get_balanced_amount(self,profile_id=None):
        if profile_id is None:
            return None
        if self.to_profile_id==profile_id:
            return 0-self.amount
        if self.from_profile_id==profile_id:
            return self.amount
        return None 
    def direction(self,profile_id):
        if self.to_profile_id==profile_id:
            return TransactionDirectionEnum.TO_PROFILE
        
        if self.from_profile_id==profile_id:
            return TransactionDirectionEnum.FROM_PROFILE
        
    def rest(self,profile_id):
        rest=0
        transactions=ProfileTransaction.objects.filter(id__lte=self.pk) 
        transactions_to=transactions.filter(to_profile_id=profile_id)
        transactions_from=transactions.filter(from_profile_id=profile_id)
        if len(transactions_to)==0:
            transactions_to={'sum':0}
        else:
            transactions_to=transactions_to.aggregate(sum=Sum('amount'))
        if len(transactions_from)==0:
            transactions_from={'sum':0}
        else:
            transactions_from=transactions_from.aggregate(sum=Sum('amount'))
        
        rest=transactions_from['sum']-transactions_to['sum']
        return rest      
    def __str__(self):
        return f'{self.title} {self.amount}'

    def get_absolute_url(self):
        return reverse("Transaction_detail", kwargs={"pk": self.pk})


class Document(Icon):
    profile=models.ForeignKey("Profile", verbose_name=_("پروفایل"), on_delete=models.CASCADE)
    file=models.FileField(_("فایل ضمیمه"),null=True,blank=True, upload_to=APP_NAME+'/Document', max_length=100)
    
    class Meta:
        verbose_name = _("Document")
        verbose_name_plural = _("اسناد")
    def get_download_url(self):
        if self.file:
            return reverse('app:download',kwargs={'document_id':self.pk})
        else:
            return ''
    def download(self):        
    #STATIC_ROOT2 = os.path.join(BASE_DIR, STATIC_ROOT)
        file_path = str(self.file.path)
        #print(file_path)
        #return JsonResponse({'download:':str(file_path)})
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app:document", kwargs={"document_id": self.pk})


    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/document/{self.pk}/change/'
   

class ResumeCategory(models.Model):
    our_team=models.ForeignKey("OurTeam", verbose_name=_("our_team"), on_delete=models.CASCADE)
    resumes=models.ManyToManyField("Resume", verbose_name=_("resume"))
    title=models.CharField(_("title"),choices=ResumeCategoryEnum.choices,default=ResumeCategoryEnum.EDUCATION, max_length=50)
    priority=models.IntegerField(_("priority"))

    class Meta:
        verbose_name = _("ResumeCategory")
        verbose_name_plural = _("دسته بندی رزومه")

    def __str__(self):
        return f'{self.our_team.name} -> {self.title}'

    def get_absolute_url(self):
        return reverse("ResumeCategory_detail", kwargs={"pk": self.pk})


class Resume(models.Model):
    priority=models.IntegerField(_("priority"))
    title=models.CharField(_("title"), max_length=50)
    subtitle=models.CharField(_("subtitle"),null=True,blank=True, max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)
    date=models.DateTimeField(_("date"), auto_now=False, auto_now_add=False)
    duration=models.CharField(_("مدت زمان"),max_length=50,null=True,blank=True)
    links=models.ManyToManyField("Link", verbose_name=_("links"),blank=True)
    documents=models.ManyToManyField("Document", verbose_name=_("documents"),blank=True)
    album=models.ForeignKey("GalleryAlbum",null=True,blank=True, verbose_name=_("آلبوم"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("Resume")
        verbose_name_plural = _("رزومه")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Resume_detail", kwargs={"pk": self.pk})


    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/resume/{self.pk}/change/'
