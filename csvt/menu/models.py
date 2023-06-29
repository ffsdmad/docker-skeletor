from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields
from mptt.models import MPTTModel, TreeForeignKey
from multiselectfield import MultiSelectField

from .managers import MenuManager

from constants import MENU_CLASSES, ICON_CLASSES


class Menu(MPTTModel, TranslatableModel):

    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    translations = TranslatedFields(
        name=models.CharField(max_length=100, blank=True),
        title=models.CharField(max_length=250, blank=True),
    )

    is_public = models.BooleanField(_("Published"), default=True)

    link = models.CharField(_("Link"), max_length=250, blank=True)
    comment = models.CharField(_("Comment"), max_length=250, blank=True)

    page = models.ForeignKey(
        "page.Page",
        on_delete=models.DO_NOTHING,
        related_name="menu",
        blank=True,
        null=True,
    )

    css_class = MultiSelectField(
        verbose_name=_('CSS Class'),
        choices=MENU_CLASSES,
        null=True, blank=True,
        max_length=100
    )

    icon_class = MultiSelectField(
        verbose_name=_('Icon Class'),
        choices=ICON_CLASSES,
        null=True, blank=True,
        max_length=100
    )

    objects = MenuManager()

    site = models.ForeignKey(
        Site,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name="menu",
    )

    on_site = CurrentSiteManager()  # Your alternative manager

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menu")

    def __str__(self):
        return self.comment
        #  ~ return self.safe_translation_getter("name", any_language=True) or self.link

    def save(self, *args, **kwargs):

        if self.site_id is None:
            if self.parent:
                self.site_id = self.parent.site_id

        super().save(*args, **kwargs)
