from app.errors import LEO_ERRORS
from django import template
register = template.Library()



@register.filter
def to_rest_color(value):
    """converts int to string"""  
    if value>0:
        return 'text-success'
    if value<0:
        return 'text-danger' 
    
    return ''
