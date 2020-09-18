from django.db.models import TextChoices
from django.utils.translation import gettext as _
from enum import Enum


class DegreeLevelEnum(TextChoices):
    DIPLOM = 'DIPLOM', _('DIPLOM')
    KARDANI = 'KARDANI', _('KARDANI')
    KARSHENASI = 'KARSHENASI', _('KARSHENASI')
    KARSHENASI_ARSHAD = 'KARSHENASI_ARSHAD', _('KARSHENASI_ARSHAD')
    PHD = 'PHD', _('PHD')


class ResumeCategoryEnum(TextChoices):
    EXPERIENCE = 'EXPERIENCE', _('EXPERIENCE')
    EDUCATION = 'EDUCATION', _('EDUCATION')
    SKILLS = 'SKILLS', _('SKILLS')
    INTERESTS = 'INTERESTS', _('INTERESTS')
    CERTIFICATIONS = 'CERTIFICATIONS', _('CERTIFICATIONS')
    AWARDS = 'AWARDS', _('AWARDS')
    WORKS_DONE = 'WORKS DONE', _('WORKS DONE')



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
    IRAN = 'IRAN', _('IRAN')
    EUROPE = 'EUROPE', _('EUROPE')
    AMERICA = 'AMERICA', _('AMERICA')
    ASIA = 'ASIA', _('ASIA')

class AddressTitleEnum(TextChoices):
    HOME = 'HOME', _('HOME')
    WORK = 'WORK', _('WORK')
    OFFICE = 'OFFICE', _('OFFICE')
    COMPANY = 'COMPANY', _('COMPANY')
    GARDEN = 'GARDEN', _('GARDEN')
    
    
class TransactionDirectionEnum(TextChoices):
    TO_PROFILE='تحویل به ',_('تحویل به ')
    FROM_PROFILE='دریافت از ',_('دریافت از ')
    
class TextDirectionEnum(TextChoices):
    Rtl='rtl',_('rtl')
    Ltr='ltr',_('ltr')

class IconsEnum(TextChoices):
    account_circle='account_circle',_('account_circle')
    add_shopping_cart='add_shopping_cart',_('add_shopping_cart')
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
    ENABLED='ENABLED',_('ENABLED')
    DISABLED='DISABLED',_('DISABLED')

class ParametersEnum(TextChoices):
    ABOUT_US_SHORT='ABOUT_US_SHORT',_('ABOUT_US_SHORT')
    ABOUT_US='ABOUT_US',_('ABOUT_US')
    MOBILE='MOBILE',_('MOBILE')
    URL='URL',_('URL')
    EMAIL='EMAIL',_('EMAIL')
    FAX='FAX',_('FAX')
    TEL='TEL',_('TEL')
    SINCE='SINCE',_('SINCE')
    LOCATION='LOCATION',_('LOCATION')
    ADDRESS='ADDRESS',_('ADDRESS')
    SLOGAN='SLOGAN',_('SLOGAN')
    ABOUT_US_TITLE='ABOUT_US_TITLE',_('ABOUT_US_TITLE')
    TITLE='TITLE',_('TITLE')
    CURRENCY='CURRENCY',_('CURRENCY')
    PRE_TILTE='PRE_TILTE',_('PRE_TILTE')
    VIDEO_TITLE='VIDEO_TITLE',_('VIDEO_TITLE')
    VIDEO_LINK='VIDEO_LINK',_('VIDEO_LINK')
    CONTACT_US='CONTACT_US',_('CONTACT_US')
    POSTAL_CODE='POSTAL_CODE',_('POSTAL_CODE')
    TERMS='TERMS',_('TERMS')
    OUR_TEAM_TITLE='OUR_TEAM_TITLE',_('OUR_TEAM_TITLE')
    OUR_TEAM_LINK='OUR_TEAM_LINK',_('OUR_TEAM_LINK')
    CSRF_FAILURE_MESSAGE='CSRF_FAILURE_MESSAGE',_('CSRF_FAILURE_MESSAGE')
    THEME_COLOR='THEME_COLOR',_('THEME_COLOR')

class MainPicEnum(TextChoices):    
    CAROUSEL='CAROUSEL',_('CAROUSEL')    
    FAQ='FAQ',_('FAQ')     
    SEARCH='SEARCH',_('SEARCH')    
    VIDEO='VIDEO',_('VIDEO')
    ABOUT='ABOUT',_('ABOUT')
    CONTACT_HEADER='CONTACT_HEADER',_('CONTACT_HEADER')
    LOGO='LOGO',_('LOGO')
    BLOG_HEADER='BLOG_HEADER',_('BLOG_HEADER')
    OUR_WORK_HEADER='OUR_WORK_HEADER',_('OUR_WORK_HEADER')
    PAGE_HEADER_DEFAULT='PAGE_HEADER_DEFAULT',_('PAGE_HEADER_DEFAULT')
    TAG_HEADER='TAG_HEADER',_('TAG_HEADER')
    ABOUT_HEADER='ABOUT_HEADER',_('ABOUT_HEADER')
class TransactionTypeEnum(TextChoices):
    CASH='CASH',_('CASH')
    CHEQUE='CHEQUE',_('CHEQUE')
    CARD='CARD',_('CARD')
    

   