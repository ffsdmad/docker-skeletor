from django.contrib import admin
#  ~ from django.contrib.sites.shortcuts import get_current_site

from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableAdmin
from parler.admin import TranslatableModelForm


from .models import Menu


class MenuAdminForm(MPTTAdminForm, TranslatableModelForm):
    pass


class MenuInline(admin.TabularInline):

    model = Menu
    form = MenuAdminForm
    show_change_link = True
    extra = 0
    raw_id_fields = ["page", ]

    #  ~ exclude = ["site"]


@admin.register(Menu)
class MenuAdmin(TranslatableAdmin, MPTTModelAdmin):

    inlines = (MenuInline, )
    list_filter = ("level", "site")
    mptt_level_indent = 20
    list_display = ("name", "link", "site")
    form = MenuAdminForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    class Media:
        css = {
             'all': ('admin/parlet-form.css',)
        }
