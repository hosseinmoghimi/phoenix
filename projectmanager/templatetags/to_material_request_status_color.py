from app.errors import LEO_ERRORS
from django import template
register = template.Library()
from projectmanager.enums import MaterialRequestStatusEnum


@register.filter
def to_material_request_status_color(value):
    """converts int to string"""  
    if value==MaterialRequestStatusEnum.INITIAL:
        return 'info'
    if value==MaterialRequestStatusEnum.DEFAULT:
        return 'danger'
    if value==MaterialRequestStatusEnum.ACCEPTED:
        return 'success'
    if value==MaterialRequestStatusEnum.IN_PROGRESS:
        return 'warning'
    if value==MaterialRequestStatusEnum.DENIED:
        return 'danger'
    if value==MaterialRequestStatusEnum.CANCELED:
        return 'secondary'
    if value==MaterialRequestStatusEnum.DELIVERED:
        return 'success'        
    
    return 'secondary'
