
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import ImageForm
from .models import make_tags_choices
from .models import (Image, UploadFile)


@admin.action(description=_("Remove CDN file"))
def update_cdn_cache(modeladmin, request, queryset):
    for obj in queryset:
        print(obj.file.clean_cache())


@admin.action(description=_("Show CDN file"))
def show_cdn_url(modeladmin, request, queryset):
    for obj in queryset:
        print(obj.file.image())


def delete_files(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


class MultiSelectFilter(admin.SimpleListFilter):

    title = _("Tags")

    parameter_name = "tags"

    template = "admin/tags_filter.html"

    def lookups(self, request, model_admin):
        return make_tags_choices()

    def value(self):
        values = self.used_parameters.get(self.parameter_name, "")
        if values:
            return values.split('|')
        return []

    def choices(self, changelist):

        for lookup, title in self.lookup_choices:

            yield {
                "selected": str(lookup) in self.value(),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }

    def queryset(self, request, queryset):

        if self.value():
            queryset = queryset.filter(
                tags__overlap=self.value()
            )
        return queryset


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class UploadFileAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)
    list_display = ("thumb", "file", "md5hash", "links")
    actions = (delete_files, )

    def has_delete_permission(self, request, obj=None):
        return False

#  ~ class ImageAdmin(TranslatableAdmin, ReverseModelAdmin):
    #  ~ inline_type = "tabular"
    #  ~ inline_reverse = ("file", )


class ImageAdmin(admin.ModelAdmin):

    form = ImageForm

    actions = (update_cdn_cache, show_cdn_url)

    list_display = ("alt", "thumb", "name", "tags_str", "created_at")
    date_hierarchy = "created_at"

    list_filter = (
        MultiSelectFilter,
    )

    readonly_fields = ["name", "created_at"]

    search_fields = ("alt", "name", "tags")

    def changelist_view(self, request, extra_context=None):
        if request.GET:
            request.GET._mutable = True
            try:
                tags = "|".join(request.GET.getlist('tags'))
                request.GET["tags"] = tags
            except KeyError as error:
                print(error)
            request.GET_mutable = False

        return super().changelist_view(request, extra_context=extra_context)

    change_form_template = 'admin/tags_change_form.html'


admin.site.register(Image, ImageAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
