from django.utils.translation import gettext as _
from django.db.models import TextChoices
class OrderStatusEnum(TextChoices):
    PROCESSING = 'درحال پردازش', _('درحال پردازش')
    COMPLETED = 'کامل شده', _('کامل شده')
    CANCELED = 'کنسل شده', _('کنسل شده')
    PENDING = 'درحال انتظار', _('درحال انتظار')
    SHIPPED = 'ارسال شده', _('ارسال شده')
    DELIVERED = 'تحویل شده', _('تحویل شده')
    PACKING = 'درحال بسته بندی', _('درحال بسته بندی')
    ACCEPTED='پذیرفته شده' , _('پذیرفته شده')
    PACKED = 'بسته بندی شده', _('بسته بندی شده')
    ON_HOLD = 'معلق', _('معلق')
    CONFIRMED = 'تایید مشتری', _('تایید مشتری')


class ProfileEnum(TextChoices):
    SUPPLIER='فروشنده',_('فروشنده')
    SHIPPER='دلیوری',_('دلیوری')
    CUSTOMER='مشتری',_('مشتری')
    # CUSTOMER='',_('')
    # CUSTOMER='',_('')