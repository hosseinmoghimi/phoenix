from django.db.models import TextChoices
from django.utils.translation import gettext as _

class PusherChannelNameEnum(TextChoices):
    NONE='NONE',_('NONE')
    SHIP='SHIP',_('SHIP')
    DELIVER='DELIVER',_('DELIVER')
    PACK='PACK',_('PACK')
    SYNC='SYNC',_('SYNC')
    SUBMIT='SUBMIT',_('SUBMIT')
    NOTIFICATION='NOTIFICATION',_('NOTIFICATION')

