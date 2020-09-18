from app.persian import PersianCalendar
from django.db import models
from .enums import UnitNameEnum,ProductRequestStatusEnum,LetterStatusEnum,AgentRoleEnum
from app.enums import ColorEnum,IconsEnum
from django.shortcuts import reverse
from app.settings import ADMIN_URL
from django.utils.translation import gettext as _
from .apps import APP_NAME
from app.models import OurWork

class WorkUnit(models.Model):
    title=models.CharField(_("title"),choices=UnitNameEnum.choices,default=UnitNameEnum.ACCOUNTING, max_length=50)
    icon=models.CharField(_("icon"),choices=IconsEnum.choices,default=IconsEnum.link, max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    employees=models.ManyToManyField("market.Employee", verbose_name=_("نیروی انسانی"),blank=True)

    class Meta:
        verbose_name = _("WorkUnit")
        verbose_name_plural = _("واحد های سازمانی")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("automation:work_unit", kwargs={"work_unit_id": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/workunit/{self.pk}/change/'

class ProductRequestSignature(models.Model):
    signature=models.ForeignKey("app.Signature", verbose_name=_("signatures"), on_delete=models.PROTECT)
    status=models.CharField(_("status"),choices=ProductRequestStatusEnum.choices,default=ProductRequestStatusEnum.REQUESTED, max_length=50)
    
    

    class Meta:
        verbose_name = _("ProductRequestSignature")
        verbose_name_plural = _("ProductRequestSignatures")

    def __str__(self):
        return f'{self.signature.profile.name()} : {self.status}'

    def get_absolute_url(self):
        return reverse("ProductRequestSignature_detail", kwargs={"pk": self.pk})

class ProductRequest(models.Model):
    employee=models.ForeignKey("market.Employee", verbose_name=_("employee"),null=True,blank=True, on_delete=models.SET_NULL)
    work_unit=models.ForeignKey("WorkUnit", verbose_name=_("واحد سازمانی"), on_delete=models.PROTECT)
    product=models.ForeignKey("market.Product", verbose_name=_("product"), on_delete=models.PROTECT)
    product_unit=models.ForeignKey("market.ProductUnit", verbose_name=_("product_unit"), on_delete=models.PROTECT)
    quantity=models.IntegerField(_("quantity"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    status=models.CharField(_("status"),choices=ProductRequestStatusEnum.choices,default=ProductRequestStatusEnum.REQUESTED, max_length=50)
    purchase_agent=models.ForeignKey("PurchaseAgent", verbose_name=_("purchase_agent"), on_delete=models.PROTECT,null=True,blank=True)
    signatures=models.ManyToManyField("ProductRequestSignature", verbose_name=_("signatures"),blank=True)
    class Meta:
        verbose_name = _("ProductRequest")
        verbose_name_plural = _("ProductRequests")

    def __str__(self):
        return f'{self.work_unit.title} / {self.product.name} : {self.quantity} {self.product_unit}'

    def get_edit_url(self):
        return ADMIN_URL+APP_NAME+'/productrequest/'+str(self.pk)+'/change/'

    def get_absolute_url(self):
        return reverse("automation:product_request", kwargs={"product_request_id": self.pk})

class PurchaseAgent(models.Model):
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    rank=models.IntegerField(_("rank"),default=0)

    class Meta:
        verbose_name = _("PurchaseAgent")
        verbose_name_plural = _("PurchaseAgents")

    def __str__(self):
        return f'{self.profile.name()} ({self.rank})'

    def get_absolute_url(self):
        return reverse("PurchaseAgent_detail", kwargs={"pk": self.pk})

class Agent(models.Model):
    profile=models.ForeignKey("app.Profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    rank=models.IntegerField(_("rank"),default=0)
    role=models.CharField(_("پست سازمانی"),choices=AgentRoleEnum.choices,default=AgentRoleEnum.DEFAULT, max_length=50)
    class Meta:
        verbose_name = _("PurchaseAgent")
        verbose_name_plural = _("مامور")

    def __str__(self):
        return f'{self.profile.name()} ({self.rank})'

    def get_absolute_url(self):
        return reverse("PurchaseAgent_detail", kwargs={"pk": self.pk})

class LetterSignature(models.Model):
    signature=models.ForeignKey("app.Signature", verbose_name=_("signatures"), on_delete=models.PROTECT)
    status=models.CharField(_("status"),choices=LetterStatusEnum.choices,default=LetterStatusEnum.DRAFT, max_length=50)
    
    

    class Meta:
        verbose_name = _("LetterSignature")
        verbose_name_plural = _("LetterSignatures")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("LetterSignature_detail", kwargs={"pk": self.pk})

class Letter(models.Model):
    sender=models.ForeignKey("app.Profile", verbose_name=_("فرستنده"), on_delete=models.CASCADE)
    work_unit=models.ForeignKey("WorkUnit", verbose_name=_("گیرنده"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    body=models.CharField(_("body"), max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    signatures=models.ManyToManyField("LetterSignature", verbose_name=_("signatures"),blank=True)
    
    class Meta:
        verbose_name = _("Letter")
        verbose_name_plural = _("Letters")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Letter_detail", kwargs={"pk": self.pk})

class Project(OurWork):
    work_units=models.ManyToManyField("WorkUnit", verbose_name=_("work_units"),blank=True)
    warehouses=models.ManyToManyField("market.WareHouse", verbose_name=_("warehouses"),blank=True)

    

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("automation:project", kwargs={"project_id": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/project/{self.pk}/change/'