from django import template
from women.models import *

register = template.Library()


@register.inclusion_tag('women/list_categories.html')
def show_category(sort=None, cat_selected=0):
    if not sort:
        categorys = Category.objects.all()
    else:
        categorys = Category.objects.order_by(sort)

    return {"categorys": categorys, "cat_selected": cat_selected}
