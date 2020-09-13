from app.errors import LEO_ERRORS
from django import template
register = template.Library()
from market.enums import OrderStatusEnum


@register.filter
def to_order_status_color(value):
    """converts int to string"""  
    if value==OrderStatusEnum.CONFIRMED:
        return 'danger'
    if value==OrderStatusEnum.ACCEPTED:
        return 'info'
    if value==OrderStatusEnum.PACKED:
        return 'danger'
    if value==OrderStatusEnum.SHIPPED:
        return 'warning'
    if value==OrderStatusEnum.DELIVERED:
        return 'success'
    if value==OrderStatusEnum.CANCELED:
        return 'secondary'
    if value==OrderStatusEnum.COMPLETED:
        return 'success'        
    
    return ''
