from app.errors import LEO_ERRORS
from django import template
register = template.Library()



@register.filter
def to_option_icon(value):
    """converts int to string"""  
    if value==1:
        return 'looks_one' 
    if value==2:
        return 'looks_two' 
    if value==3:
        return 'looks_3' 
    if value==4:
        return 'looks_4' 
    if value==5:
        return 'looks_5' 
    if value==6:
        return 'looks_6' 