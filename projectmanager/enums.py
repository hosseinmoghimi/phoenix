from django.db.models import TextChoices
from django.utils.translation import gettext as _
class ProjectStatusEnum(TextChoices):
    DEFAULT='پیش فرض',_('پیش فرض')
    IN_PROGRESS='در حال انجام',_('در حال انجام')
    INITIAL='آماده سازی اولیه',_('آماده سازی اولیه')
    DONE='انجام شده',_('انجام شده')
    DELIVERED='تحویل شده',_('تحویل شده')
    ANALYZING='درحال آنالیز',_('درحال آنالیز')

class IssyTypeEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    FORCE='FORCE',_('FORCE')
    DANGER='DANGER',_('DANGER')
    EVENT='EVENT',_('EVENT')
    WARNING='WARNING',_('WARNING')

class LogActionEnum(TextChoices):
    DEFAULT='DEFAULT',_('DEFAULT')
    DELETE='DELETE',_('DELETE')
    SAVE='SAVE',_('SAVE')
    INITIAL='INITIAL',_('INITIAL')
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
    SUPPORT='پشتیبان',_('پشتیبان')    
    SERVICEMAN='خدمات',_('خدمات')    
    DEFAULT='تایید نشده',_('تایید نشده')
    SARPARAST='سرپرست',_('سرپرست')
    KARSHENAS='کارشناس',_('کارشناس')
    MOSHAVER='مشاور',_('مشاور')
    NAZER='ناظر',_('ناظر')
    SECRETER='منشی',_('منشی')
    RECRUIT='کارآموز',_('کارآموز')
    AMIN='امین اموال',_('امین اموال')
    
class MaterialRequestStatusEnum(TextChoices):
    DEFAULT='پیش فرض',_('پیش فرض')
    INITIAL='درخواست اولیه',_('درخواست اولیه')
    ACCEPTED='پذیرفته شده',_('پذیرفته شده')
    IN_PROGRESS='در حال بررسی',_('در حال بررسی')
    DENIED='رد شده',_('رد شده')
    CANCELED='لغو شده',_('لغو شده')

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
