from django.db.models import TextChoices
from django.utils.translation import gettext as _
class UnitNameEnum(TextChoices):
    ACCOUNTING='حسابداری',_('حسابداری')
    MANAGEMENT='مدیریت',_('مدیریت')
    TRANSPORT='حمل و نقل',_('حمل و نقل')
    LOGESTIC='کارپردازی',_('کارپردازی')
    CIVIL='عمران',_('عمران')
    TASISAT='تاسیسات',_('تاسیسات')
    ENGINEERING='مهندسی',_('مهندسی')
class AgentRoleEnum(TextChoices):
    DEFAULT='پیش فرض',_('پیش فرض')
    ACCOUNTANT='حسابدار',_('حسابدار')
    MANAER='مدیریت',_('مدیریت')
    DRIVER='راننده',_('راننده')
    EXPERT='متخصص',_('متخصص')
    ENGINEER='مهندس',_('مهندس')
class ProductRequestStatusEnum(TextChoices):
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    DENIED='رد شده',_('رد شده')
    REQUESTED='درخواست شده',_('درخواست شده')
    IN_PROGRESS='در حال انجام',_('در حال انجام')
    PROCCESSING='در حال پردازش',_('در حال پردازش')    
    CANCELED='لغو شده',_('لغو شده')    
    COMPLETED='کامل شده',_('کامل شده')
class LetterStatusEnum(TextChoices):
    DRAFT='پیش نویس',_('پیش نویس')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    DENIED='رد شده',_('رد شده')
    REQUESTED='درخواست شده',_('درخواست شده')
    IN_PROGRESS='در حال انجام',_('در حال انجام')
    PROCCESSING='در حال پردازش',_('در حال پردازش')    
    CANCELED='لغو شده',_('لغو شده')    
    COMPLETED='کامل شده',_('کامل شده')
