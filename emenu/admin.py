from django.contrib import admin
from django.contrib.admin.widgets import AdminTimeWidget
from django.db import models

from emenu.models import Dish, DishCard


class DishAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TimeField: {'widget': AdminTimeWidget(format='%H:%M')},
    }


admin.site.register(Dish, DishAdmin)
admin.site.register(DishCard)
