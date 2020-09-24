from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from app.settings import ADMIN_URL,MEDIA_URL
from app.enums import DegreeLevelEnum
from app.models import OurWork
from .enums import UnitNameEnum,EmployeeEnum,ProjectStatusEnum
IMAGE_FOLDER=APP_NAME+'/images/'


class ProjectCategory(models.Model):
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
             
                {get_tag_icon}
            
              {title}</a>
          """.format(get_absolute_url=tag.get_absolute_url(),get_tag_icon=tag.icon.get_tag_icon(),title=tag.title)    
          
    class Meta:
        verbose_name = _("ProjectCategory")
        verbose_name_plural = _("ProjectCategories")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projectmanager:project_category',kwargs={'category_id':self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/projectcategory/{self.pk}/change/'


class Project(models.Model):
    pretitle=models.CharField(_("پیش عنوان"), max_length=500,blank=True,null=True)
    title=models.CharField(_("عنوان"), max_length=500,blank=True,null=True)
    posttitle=models.CharField(_("پس عنوان"), max_length=500,blank=True,null=True)
    short_description=models.TextField(_("شرح کوتاه"),blank=True,null=True)
    description=models.TextField(_("شرح کامل"),blank=True,null=True)
    action_text=models.CharField(_("متن دکمه"), max_length=100,blank=True,null=True)
    action_url=models.CharField(_("لینک دکمه"), max_length=2000,blank=True,null=True)
    video_text=models.CharField(_("متن ویدیو"), max_length=100,blank=True,null=True)
    video_url=models.CharField(_("لینک ویدیو"), max_length=2000,blank=True,null=True)
    category=models.ForeignKey("ProjectCategory",null=True,blank=True, verbose_name=_("category"), on_delete=models.SET_NULL)
    
    location=models.CharField(_('موقعیت در نقشه گوگل 400*400'),max_length=500,null=True,blank=True)    
    
    work_units=models.ManyToManyField("WorkUnit", verbose_name=_("work_units"),blank=True)
    material_warehouses=models.ManyToManyField("MaterialWareHouse", verbose_name=_("material_warehouses"),blank=True)

    status=models.CharField(_('status'),max_length=50,choices=ProjectStatusEnum.choices,default=ProjectStatusEnum.DEFAULT)
    amount=models.IntegerField(_('مبلغ'),default=0)

    def get_status_color(self):
        if self.status==ProjectStatusEnum.DEFAULT:
            return 'primary'
        if self.status==ProjectStatusEnum.INITIAL:
            return 'secondary'
        if self.status==ProjectStatusEnum.IN_PROGRESS:
            return 'info'
        if self.status==ProjectStatusEnum.DONE:
            return 'success'
        if self.status==ProjectStatusEnum.ANALYZING:
            return 'danger'
        if self.status==ProjectStatusEnum.DELIVERED:
            return 'warning'
    class Meta:
        
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projectmanager:project", kwargs={"project_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/project/{self.pk}/change/'
        
class WorkUnit(models.Model):
    title=models.CharField(_("title"),choices=UnitNameEnum.choices,default=UnitNameEnum.ACCOUNTING, max_length=50)
    employees=models.ManyToManyField("Employee", verbose_name=_("نیروی انسانی"),blank=True)
    description=models.CharField(_("description"), max_length=500,null=True,blank=True)
    class Meta:
        verbose_name = _("WorkUnit")
        verbose_name_plural = _("WorkUnits")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("automation:work_unit", kwargs={"work_unit_id": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/workunit/{self.pk}/change/'


class Employee(models.Model):
    profile=models.ForeignKey("app.Profile",related_name='emp', verbose_name=_("profile"),null=True,blank=True, on_delete=models.PROTECT)
    
    role=models.CharField(_("نقش"),choices=EmployeeEnum.choices,default=EmployeeEnum.DEFAULT, max_length=50)
    degree=models.CharField(_("مدرک"),choices=DegreeLevelEnum.choices,default=DegreeLevelEnum.KARSHENASI, max_length=50)
    major=models.CharField(_("رشته تحصیلی"),null=True,blank=True, max_length=50)
    introducer=models.CharField(_("معرف"),null=True,blank=True, max_length=50)
    def __str__(self):
        return self.profile.name()
    
    def name(self):
        if self.profile is not None:
            return f'{self.profile.name()} {self.role}'
        return f'{self.role}'
    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
    
    def get_absolute_url(self):
        return reverse('app:profile',kwargs={'profile_id':self.profile.pk})
    def get_edit_url(self):
        if self.profile is not None:
            return self.profile.get_edit_url()


class MaterialBrand(models.Model):
    prefix=models.CharField(_("پیش تعریف"), max_length=200,default='',null=True,blank=True)
    name=models.CharField(_("نام برند"), max_length=50)
    description=models.CharField(_("توضیحات"), max_length=500,default='',null=True,blank=True)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Brand/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    rate=models.IntegerField(_("امتیاز"),default=0)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    url=models.CharField(_("آدرس اینترتی"),null=True,blank=True,max_length=100)
    def image(self):
        return MEDIA_URL+str(self.image_origin)
   

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse("market:brand", kwargs={"brand_id": self.pk})
        return self.url
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/brand/'+str(self.pk)+'/change/'


class MaterialCategory(models.Model):
    prefix=models.CharField(_("پیش تعریف"), max_length=200,default='',null=True,blank=True)
    name=models.CharField(_("نام دسته"), max_length=50)
    parent=models.ForeignKey("MaterialCategory", verbose_name=_("دسته بندی بالاتر"),on_delete=models.PROTECT,blank=True,null=True)
    description=models.CharField(_("توضیحات"), max_length=500,default='',null=True,blank=True)
    image_origin=models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'MaterialCategory/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
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

   
   
    class Meta:
        verbose_name = _("MaterialCategory")
        verbose_name_plural = _("MaterialCategories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("market:list", kwargs={"parent_id": self.pk})
  
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/category/'+str(self.pk)+'/change/'


class Material(models.Model):
    name=models.CharField(_("name"), max_length=50)
    brand=models.ForeignKey("MaterialBrand", verbose_name=_("brand"), on_delete=models.CASCADE)
    model=models.CharField(_("model"), max_length=50)
    category=models.ForeignKey("MaterialCategory",related_name='material_category',on_delete=models.PROTECT)
    thumbnail=models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Material/thumbnail/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    image=models.ImageField(_("تصویر 1"), upload_to=IMAGE_FOLDER+'Material/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    image2=models.ImageField(_("تصویر 2"), upload_to=IMAGE_FOLDER+'Material/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    image3=models.ImageField(_("تصویر 3"), upload_to=IMAGE_FOLDER+'Material/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Material_detail", kwargs={"pk": self.pk})


class MaterialWareHouse(models.Model):
    name=models.CharField(_("name"), max_length=50)
    location=models.CharField(_("location"),null=True,blank=True,  max_length=50)
    employees=models.ManyToManyField("Employee", verbose_name=_("employees"),blank=True)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    class Meta:
        verbose_name = _("MaterialWareHouse")
        verbose_name_plural = _("MaterialWareHouses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("MaterialWareHouse_detail", kwargs={"pk": self.pk})


class MaterialObject(models.Model):
    material=models.ForeignKey("Material", verbose_name=_("material"), on_delete=models.CASCADE)
    serial_no=models.CharField(_('serial_no'),null=True,blank=True,max_length=200)
    barcode1=models.CharField(_('barcode1'),null=True,blank=True,max_length=200)
    borcode2=models.CharField(_('barcode2'),null=True,blank=True,max_length=200)
    barcode3=models.CharField(_('barcode3'),null=True,blank=True,max_length=200)
    package_no=models.CharField(_("package_no"), null=True,blank=True,max_length=50)
    package_name=models.CharField(_("package_name"), null=True,blank=True,max_length=50)
    

    class Meta:
        verbose_name = _("MaterialObject")
        verbose_name_plural = _("MaterialObjects")

    def __str__(self):
        return f'{self.material.name} {self.serial_no if self.serial_no else "با شناسه"+str(self.pk)}'

    def get_absolute_url(self):
        return reverse("MaterialObject_detail", kwargs={"pk": self.pk})


class MaterialPackage(models.Model):
    name=models.CharField(_("name"), max_length=50)
    pack_no=models.CharField(_("pack_no"), max_length=50)
    material_objects=models.ManyToManyField("MaterialObject", verbose_name=_("material_objects"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    

    class Meta:
        verbose_name = _("MaterialPackage")
        verbose_name_plural = _("MaterialPackages")

    def __str__(self):
        return f'{self.pack_no} {self.name}'

    def get_absolute_url(self):
        return reverse("MaterialPackage_detail", kwargs={"pk": self.pk})


class MaterialLog(models.Model):
    priority=models.CharField(_("priority"), max_length=50)
    log_type=models.CharField(_("log_type"), max_length=50)
    profile=models.ForeignKey("app.Profile",related_name='profile',on_delete=models.PROTECT)
    material_object=models.ForeignKey("MaterialObject",related_name='material_object',on_delete=models.PROTECT)
    title=models.CharField(_("title"), max_length=100)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    

    class Meta:
        verbose_name = _("MaterialPackage")
        verbose_name_plural = _("MaterialPackages")

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("MaterialPackage_detail", kwargs={"pk": self.pk})



