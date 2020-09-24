from django.db.models import TextChoices
from django.utils.translation import gettext as _
class ProjectStatusEnum(TextChoices):
    DEFAULT='پیش فرض',_('پیش فرض')
    IN_PROGRESS='در حال انجام',_('در حال انجام')
    INITIAL='آماده سازی اولیه',_('آماده سازی اولیه')
    DONE='انجام شده',_('انجام شده')
    DELIVERED='تحویل شده',_('تحویل شده')
    ANALYZING='درحال آنالیز',_('درحال آنالیز')

class UnitNameEnum(TextChoices):
    ACCOUNTING='حسابداری',_('حسابداری')
    MANAGEMENT='مدیریت',_('مدیریت')
    TRANSPORT='حمل و نقل',_('حمل و نقل')
    LOGESTIC='کارپردازی',_('کارپردازی')
    CIVIL='عمران',_('عمران')
    TASISAT='تاسیسات',_('تاسیسات')
    ENGINEERING='مهندسی',_('مهندسی')
    ELECTRICAL='برق',_('برق')
    MECHANIC='مکانیک',_('مکانیک')

class EmployeeEnum(TextChoices):
    GUARD='نگهبان',_('نگهبان')      
    MANAGER='مدیر',_('مدیر')      
    TECHNICAL='فنی',_('فنی')    
    DEFAULT='تایید نشده',_('تایید نشده')
    ACCOUNTANT='حسابدار',_('حسابدار')
    CASHIER='صندوقدار',_('صندوقدار')
    

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
