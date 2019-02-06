# - Date fields are starting with `date_` prefix.
# - Custom behaviour of fields implemented in `clean_fields` method.
# - All models here are abstract
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .utils.models import slug, Choices


class DateModel(models.Model):
    """Be aware of creation and change date of a record.
    """

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True)

    class Meta:
        abstract = True


class AuthoredModel(models.Model):
    """Use a Django user as an author/owner of a record.
    - User is required.
    - Don't allow deletion of a user that owns other records.
    """

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    """Common statuses used in publishable models.
    - pending: can be useful for waiting on someone else's approval
    - draft: when you're still working in a document
    - public: when the document is public/finished and hopefully approved
    - rejected: if you're using moderation this is useful for your moderator user

    Refer to `.utils.models.Choices` for more about using this type of "choices"
    instead of the classical tuple of tuples.

    Usage in query:
    - published/public records should be `status=MyModel.STATUSES.PUBLIC`.
    """

    STATUSES = Choices(
        PENDING=_("Pending"),
        DRAFT=_("Draft"),
        PUBLIC=_("Public"),
        REJECTED=_("Rejected"),
        B="B"
    )
    status = models.CharField(
        max_length=10, choices=STATUSES, default=STATUSES.DRAFT, db_index=True
    )

    class Meta:
        abstract = True


class PublishableModel(StatusModel):
    """Controls statuses and dates of a record.
    :date_available: Control when you want to make the object available to the public.
        of course you should consider the `status` field in your queries too, example:
            Article.objects.filter(date_available__gte=timezone.now, status="public")

    Refer `StatusModel` for status management.
    """

    date_available = models.DateTimeField(
        _("Date available"), blank=True, null=True, db_index=True
    )

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        # well, you shouln't make something public without a `date_available` information
        # so let's make sure that's not happening:

        if self.status == self.STATUSES.PUBLIC and self.date_available is None:
            self.date_available = timezone.now()

    class Meta:
        abstract = True


class ExpirableModel(models.Model):
    """Controls expiration date of a record.
    Usage in query:
      - published/public records should be `date_expire__lte=timezone.now`.
    """

    date_expire = models.DateTimeField(
        _("Expiration Date"), blank=True, null=True, db_index=True
    )

    class Meta:
        abstract = True


class LiveUpdateModel(models.Model):
    """Live Updates
    - useful for publishing things first and update the document as new information appears
    - setting a expiration date should be a good idea here. (`ExpirableModel`)
    """

    is_live_updating = models.BooleanField(_("Live Updating Status"), default=False)

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """An alternative to Django's SlugField
    Why use this and not `models.SlugField`?
    A: Well, maybe you should, but here's some things I want and `models.SlugField` doesn't have:
        - I want to be able to fill the `slug` field in the html form with free text and when
            I hit "save" the text is slugified automatically.
        - I want "unique" behaviour smarter than "this slug already exists"
            - check `core.utils.slug.Slug` and look for `unique_for_fields`
        - I want something like `django.contrib.admin.ModelAdmin.prepopulated_fields` but in the model level.
            - check `core.utils.slug.Slug` and look for `source_fields`
    """

    slug = models.CharField(_("Slug"), blank=True, max_length=140, db_index=True)
    slug_source_fields = ()
    slug_unique_for_fields = ()

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        # You could use this in a lot of places
        # Views, Forms or even other Model methods
        # You just need the Model instance available
        self.slug = slug(self)

    class Meta:
        abstract = True


class ChannelModel(models.Model):
    """Channels are like categories, sections or whatever you need to categorize something.
    """

    name = models.CharField(_("Channel Name"), max_length=60)
    description = models.TextField(_("Description"), null=True, blank=True)
    order = models.PositiveSmallIntegerField(_("Order"), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class BasicArticleModel(DateModel, PublishableModel, AuthoredModel, SlugModel):
    """Basic Article/Post
    - Refer to `PublishableModel` in order to understand about publishing controls. (statuses and dates)
    - Refer to `AuthoredModel` for `Article.author`.

    :title: Article title
    :seo_title: SEO friendly title. Useful for metatags, sharing title, HTML tag `<title>` and others.
    :hat: Short text for capturing the attention of the reader, almost like a post category/tag/hashtag.
    :short_description: Useful for social sharing and article description right after the title.
    :body: Article main text. If you will use Markdown or something that needs to be rendered
           as HTML before presentign, consider use `body` for the rendered text and create a `body_markdown`
           to store your original Markdown code.
    :notes: Useful for keeping notes about the progress of your writting, avoid taking notes on `body`.
    :featured: Control if your Article deserves the spotlight. Useful for Homepages.
    :source: Article source.
    """

    title = models.CharField(_("Title"), max_length=140, db_index=True)
    seo_title = models.CharField(
        _("SEO Title"),
        max_length=140,
        blank=True,
        null=True,
        help_text=_("SEO friendly title, will replace original title when sharing."),
    )
    hat = models.CharField(_("Hat"), max_length=60, null=True, blank=True)
    short_description = models.CharField(
        _("Short Description"), max_length=240, null=True, blank=True
    )
    body = models.TextField(_("Body Text"))
    notes = models.TextField(
        _("Internal notes"),
        null=True,
        blank=True,
        help_text=_("Internal notes only, should't be public."),
    )
    featured = models.BooleanField(_("Featured"), default=False)
    source = models.CharField(_("Source"), max_length=140, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
