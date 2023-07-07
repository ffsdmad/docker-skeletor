from django import forms
from django.forms.widgets import SelectMultiple

from .models import Image, UploadFile
from .models import make_tags_choices


class FileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ImageForm(forms.ModelForm):

    extra_tags = forms.CharField(required=False)

    upload_file = MultipleFileField(required=False)

    class Meta:
        model = Image
        exclude = ["file", ]

    def save(self, commit=False):

        tags = self.cleaned_data.get("tags", [])
        extra_tags = self.cleaned_data.get("extra_tags", None)
        if extra_tags:
            tags = [*[s.strip() for s in extra_tags.split(",")], *tags]

        instance = super().save(commit=False)
        instance.tags = tags

        for _file in self.files.getlist("upload_file"):

            file = UploadFile(file=_file)

            try:
                md5hash = UploadFile().calc_md5(_file)
                file = UploadFile.objects.get(md5hash=md5hash)
            except Exception:
                file = UploadFile(file=_file)
                file.save()

            instance.id = None

            instance.name = _file.name
            instance.file = file
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
