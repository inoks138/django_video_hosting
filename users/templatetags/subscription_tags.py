from django import template

register = template.Library()


@register.simple_tag
def get_months_case(months):
    string_value = str(months)
    if months == 1 or (not string_value.endswith('11') and months % 10 == 1):
        return f'{months} месяц'
    elif months == 2 or months == 3 or months == 4 or \
            (not string_value.endswith('12') and months % 10 == 2) or \
            (not string_value.endswith('13') and months % 10 == 3) or \
            (not string_value.endswith('14') and months % 10 == 4):
        return f'{months} месяца'
    else:
        return f'{months} месяцев'
