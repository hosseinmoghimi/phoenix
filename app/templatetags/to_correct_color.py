

from django import template
register = template.Library()


@register.filter
def to_correct_color(value):
    """converts int to string"""  
    return 'success' if value==True else 'danger'