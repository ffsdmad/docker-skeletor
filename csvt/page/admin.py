from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from django.db.models import JSONField
from jsoneditor.forms import JSONEditor


from parler.admin import TranslatableAdmin

from .models import Page, Layer, ProductLayer


class PageProduct(Page):
    class Meta:
        proxy = True
        verbose_name = _("Продуктовая страница")
        verbose_name_plural = _("Продуктовые cтраницы")


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

@admin.action(description=_("Enable user"))
def make_published(modeladmin, request, queryset):
    queryset.update(is_public=True)


@admin.action(description=_("Disable user"))
def make_disabled(modeladmin, request, queryset):
    queryset.update(is_public=False)


class PageAdmin(TranslatableAdmin):
    inlines = (LayerInline, )

    actions = (make_published, make_disabled)

    formfield_overrides = {
        JSONField: {
            "widget": JSONEditor()
        }
    }

    list_filter = ("is_public", "is_test", "is_preview")

    search_fields = (
        "slug",
        "translations__name",
        "translations__title",
    )

    list_display = ("slug", "name", "title", "image_tag")

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
                    ("title", "short_content"),
                    ("content", ),
                    ("content_mobile", ),
                    ("external_video", ),
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

    class Media:
        css = {
             'all': ('admin/parlet-form.css',)
        }


class PageProductAdmin(PageAdmin):
    inlines = (ProductLayerInline, )


admin.site.register(Page, PageAdmin)
#  ~ admin.site.register(PageProduct, PageProductAdmin)
