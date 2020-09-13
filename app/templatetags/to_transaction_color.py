from app.errors import LEO_ERRORS
from django import template
register = template.Library()
from app.enums import TransactionDirectionEnum



@register.filter
def to_transaction_color(value):
    """converts int to string"""  
    if value==TransactionDirectionEnum.TO_PROFILE:
        return 'text-danger' 
    if value==TransactionDirectionEnum.FROM_PROFILE:
        return 'text-success'
    return LEO_ERRORS.error_to_transaction_color_template_tag

