from django import forms
from django.contrib import admin
from django.forms.widgets import SelectMultiple
from django.utils.translation import gettext_lazy as _

from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm
from django_reverse_admin import ReverseModelAdmin

from .models import make_tags_choices
from .models import (Image, UploadFile)


class CsvtSelectMultiple(SelectMultiple):
    template_name = "forms/widgets/select.html"


class MultiSelectFilter(admin.SimpleListFilter):

    title = _("Tags")

    parameter_name = "tags"

    template = "admin/tags_filter.html"

    def __init__(self, request, params, model, model_admin):
        #  ~ raise None
        #  ~ if self.parameter_name in request.GET:

            #  ~ value = request.GET.getlist("tags")
            #  ~ params[self.parameter_name] = value

        super().__init__(request, params, model, model_admin)


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


class ImageForm(TranslatableModelForm):

    extra_tags = forms.CharField(required=False)

    def save(self, commit=True):

        instance = super().save(commit=commit)

        extra_tags = self.cleaned_data.get("extra_tags", None)
        if extra_tags:
            tags = self.cleaned_data.get("tags", [])
            tags = [*[s.strip() for s in extra_tags.split(",")], *tags]
            instance.tags = tags
            instance.save()
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"] = forms.MultipleChoiceField(
            choices=make_tags_choices(),
            required=False,
            widget=SelectMultiple(
                attrs=dict(style="width: 40em; height: 20em"),
            )
        )


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class UploadFileAdmin(admin.ModelAdmin):
    inlines = (ImageInline,)
    list_display = ("thumb", "file", "md5hash", "links")


class ImageAdmin(TranslatableAdmin, ReverseModelAdmin):
    inline_type = "tabular"
    inline_reverse = ("file", )
    form = ImageForm

    list_display = ("alt", "thumb", "name", "tags_str", "created_at")
    list_filter = (
        MultiSelectFilter,
    )

    search_fields = ("translations__alt", "name", "tags")

    def changelist_view(self, request, extra_context=None):
        if request.GET:
            request.GET._mutable=True
            try:
                tags = "|".join(request.GET.getlist('tags'))
                request.GET["tags"] = tags
            except KeyError as error:
                print(error)
            request.GET_mutable=False

        return super().changelist_view(request, extra_context=extra_context)

    change_form_template = 'admin/tags_change_form.html'


admin.site.register(Image, ImageAdmin)
admin.site.register(UploadFile, UploadFileAdmin)
