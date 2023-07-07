from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from jsoneditor.forms import JSONEditor

from .models import User


jsoneditor = JSONEditor(
    attrs={"cols": "40", "rows": "10", "height": "200px", "width": "600px"}
)

jsoneditor.jsoneditor_options = {
    "mode": "tree",
    "modes": ["code", "form", "text", "tree", "view"]  # // all modes
}


@admin.action(description=_("Enable user"))
def make_published(modeladmin, request, queryset):
    queryset.update(is_active=True)


@admin.action(description=_("Disable user"))
def make_disabled(modeladmin, request, queryset):
    queryset.update(is_active=False)


class CustomUserAdmin(UserAdmin):
    ordering = ("email", )

    actions = (make_published, make_disabled)

    list_filter = (
        "is_staff", "is_superuser", "is_active",
        "user_type", "accepted_rules"
    )

    list_display = (
        "username", "email", "first_name", "last_name", "is_active",
        "is_staff", "user_type"
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Contacts", {"fields": (
            "email", "phone_num",
            "addition_phone", "country", "city", "address")}),
        ("Permissions", {"fields": (
            "is_active", "is_staff",
            "is_superuser", "groups", "user_permissions", )}),
        ("CSVT Profile", {"fields": (
            "user_type", "accepted_rules",
            "rating", "id1c")}),
        ("CSVT Attributes", {
            "fields": ("attributes", ), "classes": ("collapse in", )}),

        ("Important dates", {"fields": ("date_joined", "last_login", )}),
    )

    formfield_overrides = {
        JSONField: {
            "widget": jsoneditor
        }
    }


admin.site.register(User, CustomUserAdmin)
