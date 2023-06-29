from django.contrib import admin
from django.contrib.sites.models import Site

from .models import SiteConf
from menu.admin import MenuInline

admin.site.unregister(Site)


class SiteConfInline(admin.StackedInline):
    model = SiteConf

    fieldsets = (
        (None, {"fields": (
                    "title", "keywords",
                    "description",
                    "template_name",
                    "is_public",
                ),
            }
        ),
    )


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    inlines = (SiteConfInline, MenuInline)

    list_display = (
        "domain", "name", "get_is_public", "id"
    )

    list_filter = ("siteconf__is_public",)

    search_fields = ("name", "domain",)

    def get_is_public(self, obj):
        return obj.siteconf.is_public

    get_is_public.short_description = SiteConf._meta.get_field('is_public').verbose_name

    class Media:
        css = {
             'all': ('admin/parlet-form.css',)
        }
