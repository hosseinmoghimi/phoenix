from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .enums import VehicleTypeEnum,VehicleColorEnum,VehicleBrandEnum
from django.db import models
from app.persian import PersianCalendar
from django.utils import timezone
from .apps import APP_NAME
from app.settings import ADMIN_URL
class Vehicle(models.Model):
    vehicle_type=models.CharField(_("نوع وسیله "),choices=VehicleTypeEnum.choices,default=VehicleTypeEnum.TAXI, max_length=50)
    brand=models.CharField(_("برند"),choices=VehicleBrandEnum.choices,default=VehicleBrandEnum.TOYOTA, max_length=50)
    name=models.CharField(_("نام"), max_length=50)
    color=models.CharField(_("رنگ"),choices=VehicleColorEnum.choices,default=VehicleColorEnum.SEFID, max_length=50)
    year=models.IntegerField(_("year"))
    plaque=models.CharField(_("پلاک"), max_length=50)
    owner=models.CharField(_("مالک"), max_length=50,null=True,blank=True)
    driver=models.CharField(_("راننده"), max_length=50,null=True,blank=True)
    description=models.CharField(_("description"), max_length=500,null=True,blank=True)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_updated=models.DateTimeField(_("date_updated"), auto_now=True, auto_now_add=False)
    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def __str__(self):
        return self.brand +' ' +self.name

    def get_absolute_url(self):
        return reverse("transport:vehicle", kwargs={"vehicle_id": self.pk})


class RequestService(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    vehicle_type=models.CharField(_("نوع وسیله "),choices=VehicleTypeEnum.choices,default=VehicleTypeEnum.TAXI, max_length=50)
    quantity=models.IntegerField(_("تعداد"),default=1)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_needed=models.DateTimeField(_("date_needed"),default=timezone.now, auto_now=False, auto_now_add=False)
    description=models.CharField(_("description"), max_length=500,null=True,blank=True)
    
    

    class Meta:
        verbose_name = _("RequestService")
        verbose_name_plural = _("RequestServices")

    def __str__(self):
        return f'{self.title} @ {PersianCalendar(date=self.date_needed).persian_date}'

    def get_absolute_url(self):
        return reverse("Service_detail", kwargs={"pk": self.pk})
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/requestservice/{self.pk}/change'
