from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from django.forms.models import BaseInlineFormSet

from jsoneditor.forms import JSONEditor

from parler.admin import TranslatableAdmin

from .models import Product
from .models import (Specifications, ProductSpecifications)


class ProductSpecificationsFormSet(BaseInlineFormSet):
    def __init__(self, queryset, instance, *args, **kwargs):
        queryset = queryset.filter(product=instance).order_by("order_num")

        query = Specifications.objects.exclude(
            id__in=queryset.values("specification_id")
        )

        kwargs['initial'] = [
            dict(specification=c, is_public=False)
            for c in query
        ]

        super().__init__(*args, queryset=queryset, instance=instance, **kwargs)


class ProductSpecificationsInline(admin.StackedInline):
    model = ProductSpecifications
    formset = ProductSpecificationsFormSet

    fieldsets = (
        (
            None, {
                "fields": (
                    (
                        "specification",
                        "value",
                        "is_public",
                        "order_num",
                    ),
                )
            }
        ),
    )

    def get_extra(self, request, instance):
        extra = Specifications.objects.count()
        if instance:
            extra -= instance.productspecifications_set.count()
        return extra


class ProductAdmin(TranslatableAdmin):
    inlines = (ProductSpecificationsInline,)

    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor()
        },
    }

    search_fields = (
        "slug",
        "translations__name",
    )

    list_filter = ("is_public", "manager_price")

    list_display = ["slug", "name", "image_tag"]

    fieldsets = (
        (
            _("Main info"), {
                "fields": (
                    (
                        "name", "slug",

                    ),

                    ("is_model", "type", "production", ),
                    ("is_public", "is_new", "is_action", ),
                    ("description", "short_description"),
                )
            }
        ),
        (
            _("Price"), {
                "fields": (
                    ("price", "price_tax", "price_opt", "manager_price", ),
                    ("count_opt", "price_old", "price_one"),
                    ("ostatok", "awaiting_supply",
                        "srok_postavki", "garantee"),
                )
            }
        ),

        (
            _("Attributes"), {
                "fields": ("attributes", ),
                "classes": ("collapse in",)
            }
        ),

        (
            _("Images"), {
                "fields": (
                    ("image", "install_image", "image_square"),
                ),
            }
        ),
    )

    class Media:
        css = {
             'all': ('admin/parlet-form.css',)
        }


class SpecificationsAdmin(TranslatableAdmin):

    list_display = (
        "id", "key", "name", "label", "component", "order_num", "unit"
    )

    list_editable = (
        "key", "order_num", "component"
    )

    fieldsets = (
        (
            None, {
                "fields": (
                    "key",
                    "name",
                    "label",
                    "order_num",
                    "component",
                    "comment",
                    "unit",
                )
            }
        ),
    )

    class Media:
        css = {
             'all': ('admin/parlet-form.css',)
        }


admin.site.register(Specifications, SpecificationsAdmin)
admin.site.register(Product, ProductAdmin)
