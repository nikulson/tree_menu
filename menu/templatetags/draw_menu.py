from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

from menu.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_path = context.request.path
    menu_items = MenuItem.objects.filter(title=menu_name).select_related('parent')
    html = '<ul>'
    for item in menu_items:
        is_active = False
        if current_path == item.url or current_path == reverse(item.url):
            is_active = True
        html += '<li class="{}">'.format('active' if is_active else '')
        html += '<a href="{}">{}</a>'.format(item.url, item.title)
        if item.children.exists():
            html += draw_submenu(item.children.all(), current_path)
        html += '</li>'
    html += '</ul>'
    return mark_safe(html)


def draw_submenu(children, current_path):
    html = '<ul>'
    for item in children:
        is_active = False
        if current_path == item.url or current_path == reverse(item.url):
            is_active = True
        html += '<li class="{}">'.format('active' if is_active else '')
        html += '<a href="{}">{}</a>'.format(item.url, item.title)
        if item.children.exists():
            html += draw_submenu(item.children.all(), current_path)
        html += '</li>'
    html += '</ul>'
    return html
