from django import template

register = template.Library()

cen = ['экспорт', 'принято', 'новые', 'медаль', 'матч', 'сет'
       ]



@register.filter()
def censor(value):
    x = ''
    i = list(value.split())
    for c in i:
        if c in cen or c.lower() in cen:
            x = x + c[0] + ('*' * (len(c) - 1)) + ' '
        else:
            x = x + c + ' '
    return f'{x}'
