from django.contrib import admin

from parler.admin import TranslatableAdmin

from .models import Image


class ImageAdmin(TranslatableAdmin):

    list_display = ("alt", "md5hash", "created_at")


admin.site.register(Image, ImageAdmin)

