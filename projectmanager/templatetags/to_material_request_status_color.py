from app.errors import LEO_ERRORS
from django import template
register = template.Library()
from projectmanager.enums import MaterialRequestStatus


@register.filter
def to_material_request_status_color(value):
    """converts int to string"""  
    if value==MaterialRequestStatus.INITIAL:
        return 'info'
    if value==MaterialRequestStatus.DEFAULT:
        return 'danger'
    if value==MaterialRequestStatus.ACCEPTED:
        return 'success'
    if value==MaterialRequestStatus.IN_PROGRESS:
        return 'warning'
    if value==MaterialRequestStatus.DENIED:
        return 'danger'
    if value==MaterialRequestStatus.CANCELED:
        return 'secondary'
    if value==MaterialRequestStatus.DELIVERED:
        return 'success'        
    
    return 'secondary'
