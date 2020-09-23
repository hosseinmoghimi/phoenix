from django.db.models import TextChoices
from django.utils.translation import gettext as _
class VehicleBrandEnum(TextChoices):
    TOYOTA='تویوتا',_('تویوتا')
    BENZ='بنز',_('بنز')
    SCANIA='اسکانیا',_('اسکانیا')
    VOLVO='ولوو',_('ولوو')
    CATERPILAR='کاترپیلار',_('کاترپیلار')
    HYUNDAI='هیوندای',_('هیوندای')
    HOWO='هووو',_('هووو')
    DONG_FENG='دانگ فنگ',_('دانگ فنگ')
    SAIPA='سایپا',_('سایپا')
    IRAN_KHODRO='ایران خودرو',_('ایران خودرو')
    XCMG='XCMG',_('XCMG')
    

class VehicleColorEnum(TextChoices):
    SEFID='سفید',_('سفید')
    SIAH='سیاه',_('سیاه')
    NOK_MEDADI='نوک مدادی',_('نوک مدادی')
    DOLPHINI='دلفینی',_('دلفینی')
    BEZH='بژ',_('بژ')
    GHERMEZ='قرمز',_('قرمز')

class VehicleTypeEnum(TextChoices):
    TRUCK='وانت',_('وانت')
    BUS='اتوبوس',_('اتوبوس')
    TAXI='تاکسی',_('تاکسی')
    GRADER='گریدر',_('گریدر')
    LOADER='لودر',_('لودر')
    TRAILER='تریلی',_('تریلی')
    CONTAINER='کانتینر',_('کانتینر')
    SEPERATOR='سپراتور',_('سپراتور')

   
    
