from django import template

register = template.Library()

@register.filter(name='calc_sum')
def calc_sum(queryset, field):
    return sum(getattr(obj, field) for obj in queryset)