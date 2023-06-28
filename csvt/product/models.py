from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from parler.models import TranslatableModel, TranslatedFields

from constants import (SUBPRODUCT_TYPES, MANAGER_PRICES)


class Specifications(TranslatableModel):

    translations = TranslatedFields(
        name = models.CharField(_("Name"), max_length=100),
        label = models.CharField(_("Label"), max_length=100, blank=True),
        unit = models.CharField(_("Unit"), max_length=40, blank=True),
    )

    key = models.CharField(_("Key"), max_length=40, blank=True)
    component = models.CharField(_("Component"), max_length=40, blank=True)

    comment = models.CharField(_("Cmment"), max_length=100, blank=True)

    order_num = models.IntegerField(_("Order num"), null=True, blank=True)

    class Meta:
        ordering = ("order_num", )
        verbose_name = _("Specifications")
        verbose_name_plural = _("Specifications")

    def __str__(self):
        return self.label


class Product(TranslatableModel):

    slug = models.SlugField(max_length=255, unique=True)

    translations = TranslatedFields(
        name=models.CharField(max_length=50),
        description=models.TextField(null=True, blank=True),

        short_description=models.CharField(
            max_length=900,
            null=True, blank=True
        ),

        price=models.PositiveIntegerField(),

        price_opt=models.PositiveIntegerField(
            _("Wholesale price"), blank=True, default=0
        ),

        count_opt=models.PositiveIntegerField(
            _("Wholesale minimum"), blank=True, default=0
        ),

        price_tax=models.PositiveIntegerField(
            _("price_tax"), null=True, blank=True
        ),

        price_old = models.PositiveIntegerField(
            null=True, blank=True
        ),

        price_one = models.PositiveIntegerField(
            null=True, blank=True
        )
    )

    ostatok = models.PositiveIntegerField(
        _("Remainder"), null=True, blank=True, default=0
    )

    awaiting_supply = models.PositiveIntegerField(
        _("Ожидаем поставку"),
        null=True, blank=True, default=0
    )

    garantee = models.CharField(
        _("Garantee"), max_length=300, null=True, blank=True
    )

    srok_postavki = models.CharField(
        _("srok postavki"), max_length=300, null=True, blank=True
    )

    material = models.CharField(
        _("Material"), max_length=300, null=True, blank=True
    )

    production = models.CharField(
        _("Production"), max_length=300, null=True, blank=True
    )

    is_public = models.BooleanField(_("Published"), default=True)
    is_model = models.BooleanField(_("Model"), default=False)
    is_action = models.BooleanField(_("Action"), default=False)
    is_new = models.BooleanField(_("New product"), default=False)

    manager_price = models.IntegerField(
        _("Manager price"),
        choices=MANAGER_PRICES,
        blank=True, null=True, default=0
    )

    attributes = JSONField(default=dict, null=True, blank=True)

    type = models.CharField(
        _("Type product"),
        max_length=30,
        choices=SUBPRODUCT_TYPES,
        null=True, blank=True
    )

    image = models.ImageField(
        max_length=500,
        blank=True, null=True
    )

    install_image = models.ImageField(
        _("Install image"), max_length=500,
        blank=True, null=True
    )

    image_square = models.ImageField(
        _("Image square"),
        max_length=700,
        blank=True, null=True
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def image_tag(self):
        if self.image:
            style = "width: 150px; height: 150px; object-fit: cover"
            return mark_safe(
                f"""<img src="{self.image.url}" style="{style}" />"""
            )

    image_tag.short_description = _("Image")


class ProductSpecifications(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specifications, on_delete=models.CASCADE)
    value = models.CharField(_("Value"), max_length=100)

    is_public = models.BooleanField(_("Published"), default=True)

    order_num = models.IntegerField(_("Order num"), null=True, blank=True)

    class Meta:
        verbose_name = _("Product feature")
        verbose_name_plural = _("Product specifications")

    def __str__(self):
        return f"{self.specification.label}: {self.value}"
