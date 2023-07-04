from django import forms
from django.contrib import admin
from django.forms.widgets import SelectMultiple

from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from constants import TAG_UPLOADS
from .models import make_tags_choices
from .models import Image, ChoiceArrayField


class CsvtSelectMultiple(SelectMultiple):
    template_name = "forms/widgets/select.html"



class MultiSelectFilter(admin.SimpleListFilter):
    # Filter title
    title = 'Tags'

    # model field
    parameter_name = 'tags'

    def lookups(self, request, model_admin):
        return make_tags_choices()

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(tags__contains="{}{}{}".format('{', self.value(), '}'))
        return queryset


class ImageForm(TranslatableModelForm):

    #  ~ alt = forms.CharField(required=True)
    extra_tags = forms.CharField(required=False)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        file = self.cleaned_data.get("file", None)
        print(dir(file))

        extra_tags = self.cleaned_data.get("extra_tags", None)
        if extra_tags:
            tags = self.cleaned_data.get("tags", [])
            tags = [*[s.strip() for s in extra_tags.split(',')], *tags]
            instance.tags = tags
            instance.save()

        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.MultipleChoiceField(
            choices=make_tags_choices(),
            widget=SelectMultiple(attrs=dict(style="width: 40em; height: 20em"),)
        )


class ImageAdmin(TranslatableAdmin):

    list_display = ("alt", "name", "tags_str", "md5hash", "created_at")
    list_filter = (MultiSelectFilter, )

    form = ImageForm

    #  ~ formfield_overrides = {
        #  ~ ChoiceArrayField: {
            #  ~ "widget": SelectMultiple(
                #  ~ choices=make_tags_choices(),
                #  ~ attrs=dict(style="width: 40em; height: 20em"),

            #  ~ )
        #  ~ }
    #  ~ }


admin.site.register(Image, ImageAdmin)
