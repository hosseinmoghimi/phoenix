from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from app.settings import ADMIN_URL,MEDIA_URL,SITE_URL
from app.enums import DegreeLevelEnum,ColorEnum,IconsEnum
from app.models import OurWork
from django.contrib.auth.models import Group
from app.get_username import get_username
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.contrib.contenttypes.models import ContentType
from .enums import AssignmentStatusEnum,IssueTypeEnum,UnitNameEnum,EmployeeEnum,ProjectStatusEnum,LogActionEnum,MaterialRequestStatusEnum
from django.db.models import Count
from django.db.models import Subquery
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
        verbose_name_plural = _("PageLogs - لاگ های صفحات")

    def __str__(self):
        return f'{self.manager_page_id} - {self.page if self.page else ""} - {self.action} - {self.name} - {self.profile.name() if self.profile else ""}'

    def get_absolute_url(self):
        return reverse("PageLog_detail", kwargs={"pk": self.pk})


class ManagerPage(models.Model):
    parent=models.ForeignKey("ManagerPage",related_name='parent_page',null=True,blank=True, verbose_name=_("parent"), on_delete=models.SET_NULL)
   
    location=models.CharField(_('موقعیت در نقشه گوگل'),max_length=500,null=True,blank=True)    
    
    title=models.CharField(_("عنوان"), max_length=100)
    pretitle=models.CharField(_("پیش عنوان"),null=True,blank=True, max_length=100)
    posttitle=models.CharField(_("پس عنوان"),null=True,blank=True, max_length=100)


    short_description=tinymce_models.HTMLField(_("شرح کوتاه"),blank=True,null=True)
    description=tinymce_models.HTMLField(_("شرح کامل"),blank=True,null=True)
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
    child_class=models.CharField(_("child_class"), max_length=50,null=True,blank=True)
    app_name=models.CharField(_("app_name"), max_length=50,default=APP_NAME)
    
    color=models.CharField(_('رنگ'),max_length=50,choices=ColorEnum.choices,default=ColorEnum.PRIMARY)
    icon=models.CharField(_('آیکون'),max_length=50,choices=IconsEnum.choices,default=IconsEnum.description)
    def get_icon(self):
        return f'<i class="material-icons">{self.icon}</i>'
    def get_colored_icon(self):
        return f'<i class="material-icons text-{self.color}">{self.icon}</i>'
    
    def childs(self):
        return ManagerPage.objects.filter(parent=self)
    
    def get_link(self):
        return f"""
        <a class="d-block mb-2 text-{self.color}" href="{self.get_absolute_url()}">
    {self.get_colored_icon()}
      {self.title}</a>
        """
    def save(self):
        if self.child_class is None:
            self.child_class='managerpage'
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

    def issues(self):
        return Issue.objects.filter(page=self)

    def image_header(self):
        if self.image_header is None:
            return None
        return MEDIA_URL+str(self.image_header_origin)
    def get_breadcrumb_url(self):
        if self.parent is None:
            return f"""<div class="d-inline"><a href="{self.get_absolute_url()}">&nbsp;{self.title}&nbsp;</a></div>"""
        else:
            return self.parent.get_breadcrumb_url()+f"""<span class="text-secondary">&nbsp;/&nbsp;</span><div class="d-inline"><a  href="{self.get_absolute_url()}">&nbsp;{self.title}&nbsp;</a></div>"""
    
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

    def cast(self):
        return self.real_type.get_object_for_this_type(pk=self.pk)

    def _get_real_type(self):
        return ContentType.objects.get_for_model(type(self))

    class Meta:
        verbose_name = _("ManagerPage")
        verbose_name_plural = _("ManagerPages - صفحات")
    def get_absolute_url(self):
        # child_classes=['project','work_unit','materialrequest']
        # for child_class in child_classes:
        #     if self.child_class==child_class:
        #         return f'{ADMIN_URL}{APP_NAME}/{child_class}/{self.pk}/change/'
        
        return f'{SITE_URL}{self.app_name}/{self.child_class}/{self.pk}/'
    
    def get_edit_url(self):
        return f'{ADMIN_URL}{self.app_name}/{self.child_class}/{self.pk}/change/'


class Assignment(ManagerPage):
    assign_to=models.ForeignKey("Employee",verbose_name="کاربر مربوط",on_delete=models.PROTECT)
    status=models.CharField(_('status'),max_length=50,choices=AssignmentStatusEnum.choices,default=AssignmentStatusEnum.DEFAULT)
    
    def save(self):
        self.child_class='assignment'
        self.app_name=APP_NAME
        super(Assignment,self).save()
    class Meta:
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments - تکلیف ها")

    def __str__(self):
        return f'{self.title} - {self.assign_to.profile.name()}'


class Image(models.Model):
    name=models.CharField(_("name"), max_length=50)
    image_origin=models.ImageField(_("Image"),null=True,blank=True, upload_to=IMAGE_FOLDER+'Page/Images/', height_field=None, width_field=None, max_length=None)
    thumbnail=models.ImageField(_("thumbnail"), upload_to=IMAGE_FOLDER+'Page/thumbnails/', height_field=None, width_field=None, max_length=None,blank=True,null=True)
    priority=models.IntegerField(_("ترتیب"),default=100)
    
    def image(self):
        return MEDIA_URL+str(self.image_origin)

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images - تصویر ها")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return MEDIA_URL+str(self.image_origin)

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/image/{self.pk}/change'


class ProjectCategory(ManagerPage):
     
    
    def save(self):
        self.child_class='projectcategory'
        super(ProjectCategory,self).save()
    
    class Meta:
        verbose_name = _("ProjectCategory")
        verbose_name_plural = _("ProjectCategories - دسته بندی پروژه ها")


    def get_absolute_url(self):
        return reverse('projectmanager:project_category',kwargs={'category_id':self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/projectcategory/{self.pk}/change/'


class Project(ManagerPage):
    category=models.ForeignKey("ProjectCategory",null=True,blank=True, verbose_name=_("category"), on_delete=models.SET_NULL)
    
    
    work_units=models.ManyToManyField("WorkUnit", verbose_name=_("work_units"),blank=True)
    material_warehouses=models.ManyToManyField("MaterialWareHouse", verbose_name=_("material_warehouses"),blank=True)
    contractors=models.ManyToManyField("Contractor", verbose_name=_("contractors"),blank=True)

    status=models.CharField(_('status'),max_length=50,choices=ProjectStatusEnum.choices,default=ProjectStatusEnum.DEFAULT)
    amount=models.IntegerField(_('مبلغ'),default=0)
    
    def save(self):
        self.child_class='project'
        super(Project,self).save()
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
        verbose_name_plural = _("Projects - پروژه ها")

    def __str__(self):
        return str(self.priority)+' - '+self.title
    def full_title(self):
        if self.parent is not None:
            return self.parent.full_title()+' : '+self.title
        return self.title
    def get_absolute_url(self):
        return reverse("projectmanager:project", kwargs={"project_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/project/{self.pk}/change/'
    def get_avo_url(self):
        return reverse("projectmanager:project_avo", kwargs={"project_id": self.pk})
    

class WorkUnit(ManagerPage): 
    
    def save(self):
        self.child_class='workunit'
        super(WorkUnit,self).save()
    
    def get_template(self):
        work_unit=self
        template= f"""
        <div>
        <h4 class="mt-4">
            <a class="text-{self.color} mb-2" href="{work_unit.get_absolute_url()}">
               {self.get_colored_icon()}
                {work_unit.title}</a>  
         </h4>
        """
        for employee in work_unit.employee_set.all():
            template+=f"""
                <div class="">
                    <small>
                        <a class="d-inline ml-5 text-secondary" href="{employee.profile.get_absolute_url()}">
                        <i class="fa fa-user"></i>
                        {employee.profile.name()}</a>

                        <span class="badge badge-info">{employee.role}</span>
                    </small>
                </div>
            """
        template+="""
        <hr>
        <div class="ml-5">
        """
        for work_unit1 in work_unit.childs():
            template+=work_unit1.get_template()
        template+="""
        </div>
        """


        template+='</div>'
        return template
    def employees(self):
        return Employee.objects.filter(work_unit=self)
    def childs(self):
        return WorkUnit.objects.filter(parent=self)
    class Meta:
        verbose_name = _("WorkUnit")
        verbose_name_plural = _("WorkUnits - واحد های سازمانی")

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
        return self.profile.name()+' '+self.role+((' '+self.work_unit.title) if self.work_unit else '')
    

    def my_assignments(self):
        return Assignment.objects.filter(assign_to=self)

    def save(self):
        if self.profile.user:
            # self.profile.user.groups.delete()
            pass
        if self.work_unit and self.profile.user:
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
        verbose_name_plural = _("Employees - کارکنان")
    
    def get_absolute_url(self):
        return reverse('app:profile',kwargs={'profile_id':self.profile.pk})
    def get_edit_url(self):
        if self.profile is not None:
            return self.profile.get_edit_url()


class MaterialBrand(ManagerPage):
    
    def save(self):
        self.child_class='materialbrand'
        super(MaterialBrand,self).save()
    rate=models.IntegerField(_("امتیاز"),default=0)    
    url=models.CharField(_("آدرس اینترتی"),null=True,blank=True,max_length=100)


    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands - برند های متریال")

 

    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/brand/'+str(self.pk)+'/change/'


class MaterialCategory(ManagerPage):
    
    def save(self):
        self.child_class='materialcategory'
        super(MaterialCategory,self).save()
    
    rate=models.IntegerField(_("امتیاز"),default=0)
    def materials(self):
        return Material.objects.filter(category=self)
    
   
    class Meta:
        verbose_name = _("MaterialCategory")
        verbose_name_plural = _("MaterialCategories - دسته بندی های متریال")


    def get_absolute_url(self):
        return reverse("projectmanager:material_category", kwargs={"category_id": self.pk})
  
    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/materialcategory/'+str(self.pk)+'/change/'


class Material(ManagerPage):
    
    def save(self):
        self.child_class='material'
        super(Material,self).save()
    brand=models.ForeignKey("MaterialBrand",null=True,blank=True,verbose_name=_("brand"), on_delete=models.CASCADE)
    model=models.CharField(_("model"),null=True,blank=True, max_length=50)
    category=models.ForeignKey("MaterialCategory",related_name='material_category',on_delete=models.PROTECT)
    unit_name=models.CharField(_('واحد'),null=True,blank=True,max_length=50)
    
     

    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materials -  متریال ها")


    def get_absolute_url(self):
        return reverse("projectmanager:material", kwargs={"material_id": self.pk})


class MaterialWareHouse(ManagerPage):
    
    def save(self):
        if self.location:
            self.location=self.location.replace('width="600"','width="100%"')
            self.location=self.location.replace('height="450"','height="400"')
        
        self.child_class='materialwarehouse'
        super(MaterialWareHouse,self).save()
    employees=models.ManyToManyField("Employee", verbose_name=_("کارکنان"),blank=True)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=50)
    class Meta:
        verbose_name = _("MaterialWareHouse")
        verbose_name_plural = _("MaterialWareHouses - انبار های متریال")

    def materials(self):
        materialinstock_set=self.materialinstock_set.all()
        # MaterialObject.objects.filter(id__in=self.materialinstock_set.values('material_object_id'))
        # materials=materialobject_set.all()
        return materialinstock_set.order_by('material_object')
    def materials3(self):
        materialinstock_set=self.materialinstock_set.all()
        # materialobject_set=MaterialObject.objects.filter(id__in=list(materialinstock_set.values('material_object_id')))
        # material_set=materialobject_set.only('material')
        # MaterialObject.objects.filter(id__in=self.materialinstock_set.values('material_object_id'))
        # materials=materialobject_set.all()
        materialobjects = MaterialObject.objects.filter(
            id__in=materialinstock_set.values('material_object_id')
        )

        materials=Material.objects.all().annotate(
        most_benevolent_hero=Subquery(
                materialobjects.values('material')[:1]
            )
        )

        materials=materialobjects.annotate(
        most_benevolent_hero=Count('material')
        )

        return materials
    def materials2(self):
        materialinstock_set=self.materialinstock_set.all()
        # materialobject_set=MaterialObject.objects.filter(id__in=list(materialinstock_set.values('material_object_id')))
        # material_set=materialobject_set.only('material')
        # MaterialObject.objects.filter(id__in=self.materialinstock_set.values('material_object_id'))
        # materials=materialobject_set.all()
        materialobjects = MaterialObject.objects.filter(
            id__in=materialinstock_set.values('material_object_id')
        )
        materials=materialobjects.raw('SELECT COUNT(*) AS count1,id,material_id FROM projectmanager_materialobject GROUP BY material_id')
        materials1=Material.objects.all().annotate(
        most_benevolent_hero=Subquery(
                materialobjects.values('material')[:1]
            )
        )

        materials1=materialobjects.annotate(
        most_benevolent_hero=Count('material')
        )

        return materials


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
        verbose_name_plural = _("MaterialObjects- متریال های موجود")

    def __str__(self):
        return f'{self.material.title} {self.serial_no if self.serial_no else "با شناسه"+str(self.pk)}'

    def get_absolute_url(self):
        return reverse('projectmanager:materialobject',kwargs={'materialobject_id':self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/materialobject/{self.pk}/change/'


class MaterialPackage(models.Model):
    
    pack_no=models.CharField(_("pack_no"), max_length=50)
    material_objects=models.ManyToManyField("MaterialObject", verbose_name=_("material_objects"))
     

    class Meta:
        verbose_name = _("MaterialPackage")
        verbose_name_plural = _("MaterialPackages - پکیج های متریال")

    def __str__(self):
        return f'{self.pack_no} {self.name}'

    def get_absolute_url(self):
        return reverse("MaterialPackage_detail", kwargs={"pk": self.pk})


class MaterialInStock(models.Model):
    material_object=models.ForeignKey("MaterialObject", verbose_name=_("متریال"), on_delete=models.CASCADE)
    warehouse=models.ForeignKey("MaterialWareHouse", verbose_name=_("انبار متریال"), on_delete=models.CASCADE)
    row=models.IntegerField(_('قفسه'))
    col=models.IntegerField(_('ردیف'))
    date_added=models.DateTimeField(_('تاریخ ثبت') , auto_now_add=True,auto_now=False)
    date_opi=models.DateTimeField(_('تاریخ opi') , auto_now_add=False,auto_now=False,null=True,blank=True)

    class Meta:
        verbose_name = _("MaterialInStock")
        verbose_name_plural = _("MaterialInStocks- متریال های موجود در انبار")

    def __str__(self):
        return str(self.pk)
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/materialinstock/{self.pk}/change'    


class MaterialLog(models.Model):
    priority=models.CharField(_("priority"), max_length=50)
    log_type=models.CharField(_("log_type"), max_length=50)
    profile=models.ForeignKey("app.Profile",related_name='profile',on_delete=models.PROTECT)
    material_object=models.ForeignKey("MaterialObject",related_name='material_object',on_delete=models.PROTECT)
    title=models.CharField(_("title"), max_length=100)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    

    class Meta:
        verbose_name = _("MaterialLog")
        verbose_name_plural = _("MaterialLogs- لاگ های متریال")

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse("MaterialPackage_detail", kwargs={"pk": self.pk})


class Contractor(models.Model):
    title=models.CharField(_('عنوان'),max_length=100)
    color=models.CharField(_('رنگ'),max_length=50,choices=ColorEnum.choices,default=ColorEnum.PRIMARY)
    icon=models.CharField(_('آیکون'),max_length=50,choices=IconsEnum.choices,default=IconsEnum.engineering)
    
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    def get_icon(self):
        return f'<i class="material-icons">{self.icon}</i>'
    def get_colored_icon(self):
        return f'<i class="material-icons text-{self.color}">{self.icon}</i>'
    
    
    def get_link(self):
        return f"""
        <a class="d-block mb-2 text-{self.color}" href="{self.get_absolute_url()}">
    {self.get_colored_icon()}
      {self.title}</a>
        """

    class Meta:
        verbose_name = _("Contractor")
        verbose_name_plural = _("Contractors - پیمانکار ها")

    def __str__(self):
        return f'{self.title}'
    def save(self):
        self.child_class='contractor1'
        super(Contractor,self).save()
    def get_absolute_url(self):
        return self.profile.get_absolute_url()


class MaterialRequest(ManagerPage):
    requested_material=models.ForeignKey("Material", verbose_name=_("material"), on_delete=models.CASCADE)
    quantity=models.IntegerField(_('تعداد'))
    unit_name=models.CharField(_('واحد'),max_length=50)
    employee=models.ForeignKey("Employee",null=True,blank=True,verbose_name="employee",on_delete=models.PROTECT)
    contractor=models.ForeignKey("Contractor",related_name='contractorrequest',null=True,blank=True,verbose_name="contractor",on_delete=models.PROTECT)
    for_project=models.ForeignKey("Project",verbose_name="project",on_delete=models.PROTECT)
    status=models.CharField(_("status"),choices=MaterialRequestStatusEnum.choices,default=MaterialRequestStatusEnum.INITIAL, max_length=50)
    signatures=models.ManyToManyField("app.Signature",blank=True, verbose_name=_("signatures"))
    
    def save(self):
        self.child_class='materialrequest'
        super(MaterialRequest,self).save()
    class Meta:
        verbose_name = _("MaterialRequest")
        verbose_name_plural = _("MaterialRequests - درخواست های متریال")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projectmanager:material_request", kwargs={"material_request_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/materialrequest/{self.pk}/change'


class Issue(ManagerPage):
    page=models.ForeignKey("ManagerPage",related_name='issueforwhatpage', verbose_name=_("issue_for"), on_delete=models.CASCADE)
    date_report=models.DateTimeField(_('date_report'),auto_now_add=False,auto_now=False)
    issue_type=models.CharField(_("نوع مشکل"),choices=IssueTypeEnum.choices,default=IssueTypeEnum.DEFAULT, max_length=50)
    def issue_type_badge_color(self):
        if self.issue_type==IssueTypeEnum.DEFAULT:
            return 'primary'
        if self.issue_type==IssueTypeEnum.EVENT:
            return 'success'
        if self.issue_type==IssueTypeEnum.DANGER:
            return 'danger'
        if self.issue_type==IssueTypeEnum.WARNING:
            return 'warning'
        if self.issue_type==IssueTypeEnum.FORCE:
            return 'info'
    def get_issue_type(self):
        return f"""
        <span class="badge badge-{self.issue_type_badge_color()}">{self.issue_type}</span>
        """
    def save(self):
        self.child_class='issue'
        return super(Issue,self).save()
    class Meta:
        verbose_name = _("Issue")
        verbose_name_plural = _("Issues - مشکلات پیش آمده")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projectmanager:issue", kwargs={"issue_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/issue/{self.pk}/change'

