from django.db.models import TextChoices
from django.utils.translation import gettext as _
from enum import Enum


class DegreeLevelEnum(TextChoices):
    DIPLOM = 'دیپلم', _('دیپلم')
    KARDANI = 'کاردانی', _('کاردانی')
    KARSHENASI = 'کارشناسی', _('کارشناسی')
    KARSHENASI_ARSHAD = 'کارشناسی ارشد', _('کارشناسی ارشد')
    PHD = 'دکتری', _('دکتری')


class ResumeCategoryEnum(TextChoices):
    EXPERIENCE = 'تجربه ها', _('تجربه ها')
    EDUCATION = 'آموزش ها', _('آموزش ها')
    SKILLS = 'مهارت ها', _('مهارت ها')
    INTERESTS = 'علاقه ها', _('علاقه ها')
    CERTIFICATIONS = 'گواهینامه ها', _('گواهینامه ها')
    AWARDS = 'جایزه ها', _('جایزه ها')
    WORKS_DONE = 'کار های انجام شده', _('کار های انجام شده')



class ColorEnum(TextChoices):
    SUCCESS = 'success', _('success')
    DANGER = 'danger', _('danger')
    WARNING = 'warning', _('warning')
    PRIMARY = 'primary', _('primary')
    SECONDARY = 'secondary', _('secondary')
    INFO = 'info', _('info')
    LIGHT = 'light', _('light')
    DARK = 'dark', _('dark')    
    ROSE = 'rose', _('rose')




class RegionEnum(TextChoices):
    KHAF = 'خواف', _('خواف')
    NASHTIFAN = 'نشتیفان', _('نشتیفان')
    SANGAN = 'سنگان', _('سنگان')
    GHASEMABAD='قاسم آباد' , _('قاسم آباد')
    TAYBAD='تایباد' , _('تایباد')
    TORBAT_JAM='تربت جام' , _('تربت جام')
    FARIMAN='فریمان' , _('فریمان')
    MASHAD='مشهد' , _('مشهد')
    TEHRAN='تهران' , _('تهران')
    TORBAT_HEYDARIYEH='تربت حیدریه' , _('تربت حیدریه')

class AddressTitleEnum(TextChoices):
    HOME = 'خانه', _('خانه')
    WORK = 'محل کار', _('محل کار')
    OFFICE = 'اداره', _('اداره')
    COMPANY = 'شرکت', _('شرکت')
    GARDEN = 'باغ', _('باغ')
    

class EmployeeEnum(TextChoices):
    GUARD='نگهبان',_('نگهبان')      
    MANAGER='مدیر',_('مدیر')      
    TECHNICAL='فنی',_('فنی')    
    DEFAULT='تایید نشده',_('تایید نشده')
    ACCOUNTANT='حسابدار',_('حسابدار')
    CASHIER='صندوقدار',_('صندوقدار')
    
    
class TransactionDirectionEnum(TextChoices):
    TO_PROFILE='تحویل به ',_('تحویل به ')
    FROM_PROFILE='دریافت از ',_('دریافت از ')
    
class TextDirectionEnum(TextChoices):
    Rtl='rtl',_('rtl')
    Ltr='ltr',_('ltr')

class IconsEnum(TextChoices):
    engineering='engineering',_('engineering')
    account_circle='account_circle',_('account_circle')
    add_shopping_cart='add_shopping_cart',_('add_shopping_cart')
    apartment='apartment',_('apartment')
    alarm='alarm',_('alarm')
    attach_file='attach_file',_('attach_file')
    attach_money='attach_money',_('attach_money')
    backup='backup',_('backup')
    build='build',_('build')
    chat='chat',_('chat')
    dashboard='dashboard',_('dashboard')
    delete='delete',_('delete')
    description='description',_('description')
    face='face',_('face')
    favorite='favorite',_('favorite')
    get_app='get_app',_('get_app')
    help_outline='help_outline',_('help_outline')
    home='home',_('home')
    important_devices='important_devices',_('important_devices')
    link='link',_('link')
    local_shipping='local_shipping',_('local_shipping')
    lock='lock',_('lock')
    mail='mail',_('mail')
    notification_important='notification_important',_('notification_important')
    psychology='psychology',_('psychology')
    publish='publish',_('publish')
    reply='reply',_('reply')
    schedule='schedule',_('schedule')
    send='send',_('send')
    settings='settings',_('settings')
    share='share',_('share')
    sync='sync',_('sync')
    vpn_key='vpn_key',_('vpn_key')

class IconFlatEnum(TextChoices):
    ZOOM='flaticon-zoom'
    VECTOR='flaticon-vector'
    WEB_PROGRAMMING='flaticon-web-programming'
    
class ProfileStatusEnum(TextChoices):
    ENABLED='فعال',_('فعال')
    DISABLED='غیر فعال',_('غیر فعال')

class ParametersEnum(TextChoices):
    NAV_TEXT_COLOR='رنگ متن منوی سایت',_('رنگ متن منوی سایت')
    GOOGLE_SEARCH_CONSOLE_TAG='تگ سرچ گوگل',_('تگ سرچ گوگل')
    ABOUT_US_SHORT='درباره ما کوتاه',_('درباره ما کوتاه')
    ABOUT_US='درباره ما کامل',_('درباره ما کامل')
    MOBILE='موبایل',_('موبایل')
    URL='لینک',_('لینک')
    EMAIL='ایمیل',_('ایمیل')
    FAX='فکس',_('فکس')
    TEL='تلفن',_('تلفن')
    LOCATION='موقعیت در گوگل مپ',_('موقعیت در گوگل مپ')     
    ADDRESS='آدرس',_('آدرس')
    SLOGAN='شرح کوتاه',_('شرح کوتاه')
    ABOUT_US_TITLE='عنوان درباره ما',_('عنوان درباره ما')
    TITLE='عنوان',_('عنوان')
    CURRENCY='واحد پول',_('واحد پول')
    PRE_TILTE='پیش عنوان',_('پیش عنوان')
    VIDEO_TITLE='عنوان ویدیو',_('عنوان ویدیو')
    VIDEO_LINK='لینک ویدیو',_('لینک ویدیو')
    CONTACT_US='ارتباط با ما',_('ارتباط با ما')
    POSTAL_CODE='کد پستی',_('کد پستی')
    TERMS='قوانین',_('قوانین')
    OUR_TEAM_TITLE='عنوان تیم ما',_('عنوان تیم ما')
    OUR_TEAM_LINK='لینک تیم ما',_('لینک تیم ما')
    CSRF_FAILURE_MESSAGE='پیام درخواست نامعتبر',_('پیام درخواست نامعتبر')
    THEME_COLOR='رنگ سربرگ کروم در موبایل',_('رنگ سربرگ کروم در موبایل')





class MainPicEnum(TextChoices):    
    FAVICON='آیکون سایت',_('آیکون سایت')     
    CAROUSEL='سایت',_('سایت')    
    FAQ='سوالات',_('سوالات')     
    SEARCH='جستجو',_('جستجو')    
    VIDEO='ویدیو',_('ویدیو')
    ABOUT='درباره ما',_('درباره ما')
    CONTACT_HEADER='سربرگ ارتباط با ما',_('سربرگ ارتباط با ما')
    LOADING='لودینگ',_('لودینگ')
    LOGO='لوگو',_('لوگو')
    BIG_LOGO='لوگوی بزرگ',_('لوگوی بزرگ')
    DARK_LOGO='لوگوی تیره',_('لوگوی تیره')
    LIGHT_LOGO='لوگوی روشن',_('لوگوی روشن')
    BLOG_HEADER='سربرگ مقاله',_('سربرگ مقاله')
    OUR_WORK_HEADER='سربرگ پروژه',_('سربرگ پروژه')
    PAGE_HEADER_DEFAULT='سربرگ پیش فرض برای صفحات',_('سربرگ پیش فرض برای صفحات')
    ABOUT_HEADER='سربرگ درباره ما',_('سربرگ درباره ما')
    TAG_HEADER='سربرگ برچسب',_('سربرگ برچسب')
    
class TransactionTypeEnum(TextChoices):
    CASH='CASH',_('CASH')
    CHEQUE='CHEQUE',_('CHEQUE')
    CARD='CARD',_('CARD')
    

   