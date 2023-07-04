from django.contrib import admin
from file.models import File, Image



class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "exturl", "title", "images")


class FileAdmin(admin.ModelAdmin):
    list_display = ("title", "url")


admin.site.register(Image, ImageAdmin)
admin.site.register(File, FileAdmin)
