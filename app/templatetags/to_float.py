from app.errors import LEO_ERRORS
from django import template
register = template.Library()



@register.filter
def to_float(value):
    """converts int to string"""  
    if value=='rtl' or value=='right':
        return 'float:right!important;' 
    if value=='ltr' or value=='left':
        return 'float:left!important;' 