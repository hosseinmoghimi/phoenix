from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from app.settings import ADMIN_URL,MEDIA_URL
from app.enums import DegreeLevelEnum
from app.models import OurWork
from django.contrib.auth.models import Group
from app.get_username import get_username
from django.contrib.auth.models import User
from .enums import UnitNameEnum,EmployeeEnum,ProjectStatusEnum,LogActionEnum,MaterialRequestStatus
IMAGE_FOLDER=APP_NAME+'/images/'

class PageLog(models.Model):
    name=models.CharField(_("name"), max_length=50)
    manager_page_id=models.IntegerField(_("manager_page_id"), default=0)
    page=models.ForeignKey("ManagerPage", verbose_name=_("page"),null=True,blank=True, on_delete=models.SET_NULL)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    profile=models.ForeignKey("app.Profile",null=True,blank=True, verbose_name=_("ایجاد کننده"), on_delete=models.CASCADE)
    description=models.CharField(_("description"),null=True,blank=True ,max_length=500)
    action=models.CharField(_("action"),choices=LogActionEnum.choices,default=LogActionEnum.DEFAULT, max_length=50)
    
    class Meta:
        verbose_name = _("PageLog")
        verbose_name_plural = _("PageLogs")

    def __str__(self):
        return f'{self.manager_page_id} - {self.page if self.page else ""} - {self.action} - {self.name} - {self.profile.name() if self.profile else ""}'

    def get_absolute_url(self):
        return reverse("PageLog_detail", kwargs={"pk": self.pk})


class ManagerPage(models.Model):
    
    title=models.CharField(_("عنوان"), max_length=100)
    pretitle=models.CharField(_("پیش عنوان"),null=True,blank=True, max_length=100)
    posttitle=models.CharField(_("پس عنوان"),null=True,blank=True, max_length=100)


    short_description=models.TextField(_("شرح کوتاه"),blank=True,null=True)
    description=models.TextField(_("شرح کامل"),blank=True,null=True)
    action_text=models.CharField(_("متن دکمه"), max_length=100,blank=True,null=True)
    action_url=models.CharField(_("لینک دکمه"), max_length=2000,blank=True,null=True)
    video_text=models.CharField(_("متن ویدیو"), max_length=100,blank=True,null=True)
    video_url=models.CharField(_("لینک ویدیو"), max_length=2000,blank=True,null=True)
    

    priority=models.IntegerField(_("ترتیب"),default=0)  

    image_header_origin=models.ImageField(_("تصویر سربرگ"),null=True,blank=True, upload_to=IMAGE_FOLDER+'Page/', height_field=None, width_field=None, max_length=None)
    images=models.ManyToManyField("Image", verbose_name=_("تصویر ها"),blank=True)
    
    meta_datas=models.ManyToManyField("app.MetaData", verbose_name=_("meta_datas"),blank=True)    
    tags=models.ManyToManyField("app.Tag", verbose_name=_("tags"),blank=True)    
    links=models.ManyToManyField("app.Link", verbose_name=_("links"),blank=True)    
    documents=models.ManyToManyField("app.Document", verbose_name=_("documents"),blank=True)    
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_updated=models.DateTimeField(_("date_updated"), auto_now_add=False, auto_now=True)
    related_pages=models.ManyToManyField("ManagerPage", verbose_name=_("related_pages"),blank=True)    
    def save(self):
        if self.priority==0:
            super(ManagerPage,self).save()
            self.priority=self.pk
            super(ManagerPage,self).save()
            return self
        # else:
        #     try:
        #         self.priority=ManagerPage.objects.get(pk=self.pk).priority
        #     except:                
        #         self.priority=self.pk
        return super(ManagerPage,self).save()


    def image_header(self):
        if self.image_header is None:
            return None
        return MEDIA_URL+str(self.image_header_origin)

    # def save(self):
    #     super(ManagerPage,self).save()
    #     username=get_username()
    #     # user=User.objects.get(username=username)
    #     # profile=ProfileRepo(user=user).me
    #     log=PageLog(page=self,manager_page_id=self.pk,name=self.title+' username:'+str(username),profile=None,action=LogActionEnum.SAVE)
    #     log.save()

    # def delete(self):
    #     super(ManagerPage,self).save()
    #     user=User.objects.get(username=get_username())
    #     profile=ProfileRepo(user=user).me
    #     log=PageLog(manager_page_id=self.pk,page=None,name=self.title,profile=profile,action=LogActionEnum.DELETE)
    #     log.save()
    #     super(ManagerPage,self).delete()

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class Image(models.Model):
    name=models.CharField(_("name"), max_length=50)
    image_origin=models.ImageField(_("Image"),null=True,blank=True, upload_to=IMAGE_FOLDER+'Page/Images/', height_field=None, width_field=None, max_length=None)
    thumbnail=models.ImageField(_("thumbnail"), upload_to=IMAGE_FOLDER+'Page/thumbnails/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    priority=models.IntegerField(_("ترتیب"),default=100)
    
    def image(self):
        return MEDIA_URL+str(self.image_origin)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return MEDIA_URL+str(self.image_origin)


class ProjectCategory(ManagerPage):
     
    

    
    class Meta:
        verbose_name = _("ProjectCategory")
        verbose_name_plural = _("ProjectCategories")


    def get_absolute_url(self):
        return reverse('projectmanager:project_category',kwargs={'category_id':self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/projectcategory/{self.pk}/change/'


class Project(ManagerPage):
    category=models.ForeignKey("ProjectCategory",null=True,blank=True, verbose_name=_("category"), on_delete=models.SET_NULL)
    parent=models.ForeignKey("Project",null=True,blank=True, verbose_name=_("parent"), on_delete=models.SET_NULL)
   
    location=models.CharField(_('موقعیت در نقشه گوگل 400*400'),max_length=500,null=True,blank=True)    
    
    
    work_units=models.ManyToManyField("WorkUnit", verbose_name=_("work_units"),blank=True)
    material_warehouses=models.ManyToManyField("MaterialWareHouse", verbose_name=_("material_warehouses"),blank=True)
    contractors=models.ManyToManyField("Contractor", verbose_name=_("contractors"),blank=True)

    status=models.CharField(_('status'),max_length=50,choices=ProjectStatusEnum.choices,default=ProjectStatusEnum.DEFAULT)
    amount=models.IntegerField(_('مبلغ'),default=0)

    def childs(self):
        return Project.objects.filter(parent=self)
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
        return str(self.priority)+' - '+self.title

    def get_absolute_url(self):
        return reverse("projectmanager:project", kwargs={"project_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/project/{self.pk}/change/'
        

class WorkUnit(ManagerPage): 

    parent=models.ForeignKey("WorkUnit",null=True,blank=True, verbose_name=_("parent"), on_delete=models.SET_NULL)
   
    
    def employees(self):
        return Employee.objects.filter(work_unit=self)
    def childs(self):
        return WorkUnit.objects.filter(parent=self)
    class Meta:
        verbose_name = _("WorkUnit")
        verbose_name_plural = _("WorkUnits")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projectmanager:work_unit", kwargs={"work_unit_id": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/workunit/{self.pk}/change/'


class Employee(models.Model):
    profile=models.ForeignKey("app.Profile",related_name='emp', verbose_name=_("profile"),null=True,blank=True, on_delete=models.PROTECT)
    work_unit=models.ForeignKey("WorkUnit", verbose_name=_("work_unit"),null=True,blank=True, on_delete=models.PROTECT)
    
    role=models.CharField(_("نقش"),choices=EmployeeEnum.choices,default=EmployeeEnum.DEFAULT, max_length=50)
    degree=models.CharField(_("مدرک"),choices=DegreeLevelEnum.choices,default=DegreeLevelEnum.KARSHENASI, max_length=50)
    major=models.CharField(_("رشته تحصیلی"),null=True,blank=True, max_length=50)
    introducer=models.CharField(_("معرف"),null=True,blank=True, max_length=50)
    def __str__(self):
        return self.profile.name()
    
    def save(self):
        group_name=self.role+' '+self.work_unit.title
        try:
            origin_group=Group.objects.get(name=group_name)
        except:
            Group.objects.filter(name=group_name).delete()
            origin_group = None
        if  origin_group is None:
            origin_group=Group(name=group_name)
            origin_group.save()
        if origin_group is not None:
                if self.profile.user is not None:
                    self.profile.user.groups.add(origin_group)
        super(Employee,self).save()

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


class MaterialBrand(ManagerPage):
    
    rate=models.IntegerField(_("امتیاز"),default=0)    
    url=models.CharField(_("آدرس اینترتی"),null=True,blank=True,max_length=100)


    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

 
    def get_absolute_url(self):
        # return reverse("market:brand", kwargs={"brand_id": self.pk})
        return self.url
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/brand/'+str(self.pk)+'/change/'


class MaterialCategory(ManagerPage):
    
    parent=models.ForeignKey("MaterialCategory", verbose_name=_("دسته بندی بالاتر"),on_delete=models.PROTECT,blank=True,null=True)
    
    rate=models.IntegerField(_("امتیاز"),default=0)
    
    
   
    class Meta:
        verbose_name = _("MaterialCategory")
        verbose_name_plural = _("MaterialCategories")


    def get_absolute_url(self):
        return reverse("market:list", kwargs={"parent_id": self.pk})
  
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/category/'+str(self.pk)+'/change/'


class Material(ManagerPage):
    
    brand=models.ForeignKey("MaterialBrand", verbose_name=_("brand"), on_delete=models.CASCADE)
    model=models.CharField(_("model"), max_length=50)
    category=models.ForeignKey("MaterialCategory",related_name='material_category',on_delete=models.PROTECT)
    
     

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials")


    def get_absolute_url(self):
        return reverse("projectmanager:material", kwargs={"material_id": self.pk})


class MaterialWareHouse(ManagerPage):
    
    location=models.CharField(_("location"),null=True,blank=True,  max_length=50)
    employees=models.ManyToManyField("Employee", verbose_name=_("employees"),blank=True)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    class Meta:
        verbose_name = _("MaterialWareHouse")
        verbose_name_plural = _("MaterialWareHouses")


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
    
    pack_no=models.CharField(_("pack_no"), max_length=50)
    material_objects=models.ManyToManyField("MaterialObject", verbose_name=_("material_objects"))
     

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


class Contractor(models.Model):
    title=models.CharField(_("title"), max_length=50)
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("Contractor")
        verbose_name_plural = _("Contractors")

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("Contractor_detail", kwargs={"pk": self.pk})


class MaterialRequest(ManagerPage):
    requested_material=models.ForeignKey("Material", verbose_name=_("material"), on_delete=models.CASCADE)
    quantity=models.IntegerField(_('تعداد'))
    unit_name=models.CharField(_('واحد'),max_length=50)
    employee=models.ForeignKey("Employee",null=True,blank=True,verbose_name="employee",on_delete=models.PROTECT)
    contractor=models.ForeignKey("Contractor",null=True,blank=True,verbose_name="contractor",on_delete=models.PROTECT)
    for_project=models.ForeignKey("Project",verbose_name="project",on_delete=models.PROTECT)
    status=models.CharField(_("status"),choices=MaterialRequestStatus.choices,default=MaterialRequestStatus.INITIAL, max_length=50)
    
    class Meta:
        verbose_name = _("MaterialRequest")
        verbose_name_plural = _("MaterialRequests")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("MaterialRequest_detail", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/materialrequest/{self.pk}/change'




