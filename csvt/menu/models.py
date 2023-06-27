from django.db import models
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields
from mptt.models import MPTTModel, TreeForeignKey
from multiselectfield import MultiSelectField

from .managers import MenuManager

from constants import MENU_CLASSES, ICON_CLASSES


class Menu(MPTTModel, TranslatableModel):

    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=True),
        title=models.CharField(max_length=250, blank=True),
    )

    is_public = models.BooleanField(_("Published"), default=True)

    link = models.CharField(_("Link"), max_length=250, blank=True)
    comment = models.CharField(_("Comment"), max_length=250, blank=True)

    page = models.ForeignKey(
        "pages.Page",
        on_delete=models.CASCADE,
        related_name="menu",
        blank=True,
        null=True,
    )

    css_class = MultiSelectField(choices=[[c, c] for c in MENU_CLASSES], blank=True)

    icon_class = MultiSelectField(choices=[[c, c] for c in ICON_CLASSES], blank=True)

    objects = MenuManager()

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menu")

    def __str__(self):
        return self.comment
        #  ~ return self.safe_translation_getter("name", any_language=True) or self.link
