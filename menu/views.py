from django.shortcuts import render
from .models import MenuItem


def menu(request, menu_name):
    menu_items = MenuItem.objects.filter(title=menu_name)
    return render(request, 'menu/menu.html', {'menu_items': menu_items})

