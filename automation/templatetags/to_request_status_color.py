from app.errors import LEO_ERRORS
from django import template
register = template.Library()
from automation.enums import ProductRequestStatusEnum


@register.filter
def to_request_status_color(value):
    """converts string to bootstrap color"""  
    if value==ProductRequestStatusEnum.REQUESTED:
        return 'primary'
    if value==ProductRequestStatusEnum.DENIED:
        return 'dark'
    if value==ProductRequestStatusEnum.ACCEPTED:
        return 'info'
    if value==ProductRequestStatusEnum.PROCCESSING:
        return 'warning'
    if value==ProductRequestStatusEnum.IN_PROGRESS:
        return 'danger'
    if value==ProductRequestStatusEnum.CANCELED:
        return 'secondary'
    if value==ProductRequestStatusEnum.COMPLETED:
        return 'success'        
    
    return ''
