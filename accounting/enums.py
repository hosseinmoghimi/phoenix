from django.db.models import TextChoices
from django.utils.translation import gettext as _

class FinancialDocument(TextChoices):
    DARAMAD='درآمد',_('درآمد')
