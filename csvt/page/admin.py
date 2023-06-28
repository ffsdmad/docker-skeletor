from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django.db.models import JSONField
from jsoneditor.forms import JSONEditor


from parler.admin import TranslatableAdmin

from .models import Page, Layer, ProductLayer


class LayerInline(admin.TabularInline):
    model = Layer
    fk_name = "parent"
    raw_id_fields = ("group", "page")


class ProductLayerInline(admin.TabularInline):
    model = ProductLayer
    fk_name = "parent"
    fileds = ("id", "title")
    raw_id_fields = ("group", "product")
    extra = 0


class PageAdmin(TranslatableAdmin):
    inlines = (LayerInline, ProductLayerInline)

    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor()
        }
    }

    search_fields = (
        "slug",
        "translations__name",
        "translations__title",
    )

    list_display = ["slug", "name", "title", "image_tag"]

    class Media:
        css = {
             'all': ('admin/parlet-form.css',)
        }

    fieldsets = (
        (
            _("Main info"), {
                "fields": (
                    (
                        "name", "is_public", "is_preview", "is_test",
                    ),
                    ("slug", "template_name",),
                )
            }
        ),
        (
            _("SEO"), {
                "classes": ("grp-collapse grp-open",),
                "fields": (
                    ("seo_description", "seo_keywords"),
                    ("seo_title", "seo_h1", "seo_h2"),
                )
            }
        ),
        (
            _("Content"), {
                "fields": (
                    ("title", ),
                    ("content", ),
                )
            }
        ),
        (
            _("Images"),
            {
                "fields": (
                    ("image", "image_square"),
                    ("image_mobile", "image_rectangle"),
                ),
            }
        ),
        (
            _("Attributes"), {
                "fields": (("attributes"), ),
                "classes": ("collapse in",)
            }
        ),
    )


admin.site.register(Page, PageAdmin)
