
from django import template
  
register = template.Library()
  
@register.filter
def ranking_delta(value):
    if value > 0:
        return f'-{value}'
    elif value == 0:
        return '-'
    else:
        return str(value)