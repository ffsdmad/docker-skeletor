from os import listdir

from django.db import models
from django.db.models import JSONField
from django.conf import settings
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField

from multiselectfield import MultiSelectField
from parler.models import TranslatableModel, TranslatedFields

from ckeditor.fields import RichTextField

from constants import LAYER_CLASSES, PRODUCT_FLAGS


class Page(TranslatableModel):

    translations = TranslatedFields(
        name=models.CharField(max_length=150),
        title=models.CharField(max_length=250, blank=True),

        content=RichTextField(
            _('Content'), config_name="default", blank=True
        ),

        content_mobile=RichTextField(
            _('Mobile content'), config_name="default", blank=True
        ),

        short_content=models.CharField(
            _('Short content'), max_length=2048, null=True, blank=True
        ),

        external_video = models.CharField(
            _('External video'), max_length=200, null=True, blank=True
        ),

        seo_h1=models.CharField(max_length=90, blank=True),
        seo_h2=models.CharField(max_length=90, blank=True),
        seo_title=models.CharField(max_length=150, blank=True),
        seo_keywords=models.CharField(max_length=900, blank=True),
        seo_description=models.CharField(max_length=900, blank=True),
    )

    comment = models.CharField(_("Comment"), max_length=100, blank=True)

    image = models.ImageField(null=True, blank=True, upload_to="images/")

    image_square = models.ImageField(
        null=True, blank=True,
        upload_to="image square/"
    )

    image_mobile = models.ImageField(
        null=True, blank=True,
        upload_to="image mobile/"
    )

    image_rectangle = models.ImageField(
        null=True,
        blank=True,
        upload_to="image rectangle/",
    )

    slug = models.SlugField(null=True)

    is_public = models.BooleanField(_("Published"), default=True)
    is_preview = models.BooleanField(_("Preview"), default=False)
    is_test = models.BooleanField(_("Test"), default=False)

    date = models.DateField(blank=True, default=None, null=True)

    attributes = JSONField(
        _("Attributes"), default=dict, null=True, blank=True
    )

    template_name = models.CharField(
        max_length=900,
        verbose_name=_("Template name"),
        choices=(
            (f, f) for f in sorted(
                listdir(settings.BASE_DIR / "templates/")
            ) if f.split(".")[-1] in ("html", "vue")
        ),
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        if self.image:
            style = "width: 150px; height: 150px; object-fit: cover"
            return mark_safe(
                f"""<img src="{self.image.url}" style="{style}" />"""
            )

    image_tag.short_description = _("Image")

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("page", kwargs=dict(slug=self.slug))


class Layer(TranslatableModel):
    parent = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="layers", null=True, blank=True
    )

    group = models.ForeignKey(
        "self", verbose_name=_("Group"),
        on_delete=models.CASCADE,
        related_name="group_list",
        null=True, blank=True
    )

    page = models.ForeignKey(
        Page,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    is_public = models.BooleanField(_("Published"), default=True)

    order_num = models.IntegerField(
        _("Order num"), null=True, blank=True
    )

    language = ArrayField(
        models.CharField(max_length=5, blank=True, default=("ru", "be", "en")),
        default=list,
        verbose_name=_("Language"),
        size=8
    )

    css_class = MultiSelectField(
        verbose_name=_('CSS Class'),
        choices=LAYER_CLASSES,
        null=True, blank=True,
        max_length=100
    )

    translations = TranslatedFields(
        title=models.CharField(max_length=300, null=True, blank=True),

        description=models.CharField(
            max_length=300, null=True, blank=True
        ),
    )

    class Meta:
        verbose_name = _("Layer")
        verbose_name_plural = _("Layers")


class ProductLayer(TranslatableModel):
    parent = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name="products", null=True, blank=True
    )

    group = models.ForeignKey(
        "self", verbose_name=_("Group"),
        on_delete=models.CASCADE,
        related_name="group_list",
        null=True, blank=True
    )

    product = models.ForeignKey(
        "product.Product",
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    is_public = models.BooleanField(_("Published"), default=True)

    order_num = models.IntegerField(
        _("Order num"), null=True, blank=True
    )

    language = ArrayField(
        models.CharField(max_length=5, blank=True, default=("ru", "be", "en")),
        default=list,
        verbose_name=_("Language"),
        size=8
    )

    css_class = MultiSelectField(
        verbose_name=_('CSS Class'),
        choices=PRODUCT_FLAGS,
        null=True, blank=True,
        max_length=100
    )

    translations = TranslatedFields(
        title=models.CharField(max_length=300, null=True, blank=True),

        description=models.CharField(
            max_length=300, null=True, blank=True
        ),
    )

    video_guide = models.CharField(
        max_length=300, null=True, blank=True
    )

    complex_count = models.IntegerField(
        _("Complex count"), default=0
    )

    class Meta:
        verbose_name = _("Product layer")
        verbose_name_plural = _("Product layers")

    def __str__(self):
        return f"{self.id} "
