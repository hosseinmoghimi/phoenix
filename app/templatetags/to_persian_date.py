from django import template
register = template.Library()
from app.persian import PersianCalendar

@register.filter
def to_persian_date(value):
    try:    
        a=PersianCalendar().from_gregorian(value)        
        return f'<span title="{value.strftime("%Y/%m/%d %H:%M:%S") }">{str(a)}</span>'
    except:
        return None
