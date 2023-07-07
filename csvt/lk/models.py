import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.db.models import JSONField

from constants import USER_TYPES, USER


class User(AbstractUser):

    phone_num = models.CharField(_("Phone"), max_length=20)

    addition_phone = models.CharField(
        _("Add. phone"),
        max_length=40,
        default="", blank=True
    )

    country = models.CharField(
        _("Country"),
        max_length=300,
        null=True, blank=True
    )

    city = models.CharField(
        _("City"),
        max_length=300,
        null=True, blank=True
    )

    address = models.CharField(
        _("Address"),
        max_length=200,
        null=True, blank=True)

    user_type = models.CharField(
        _("User type"), max_length=10,
        choices=USER_TYPES, default=USER
    )

    is_block = models.BooleanField(_("Is block"), default=False)

    accepted_rules = models.BooleanField(
        _("Accepted rules"),
        default=False
    )

    attributes = JSONField(
        _("Attributes"),
        default=dict, null=True, blank=True
    )

    rating = models.IntegerField(
        _("Rating"), default=0
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    id1c = models.UUIDField(
        _("1C id"),
        null=True,
        blank=True,
        editable=True
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        swappable = "AUTH_USER_MODEL"
