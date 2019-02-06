from django.utils.text import slugify

# Slug Helpers


def add_counter_to_slug(slug, counter_separator="_"):
    """Add a counter to a given slug or increment the existent counter by 1
    Based on a `counter_separator` we'll discover if the current slug
    already has a `counter`.

    Example:
        slug = "1_article-abouth-something"
        1: counter
        _: counter_separator
        article-abouth-something: slug without counter

        After processing: "2_article-abouth-something"

    In case we receive a slug with no counter, for example: "article-abouth-something"
    we simply add the counter value and the `counter_separator` as prefix:
    "1_article-abouth-something"
    """
    splitted_slug = slug.split(counter_separator)
    if len(splitted_slug) > 1 and splitted_slug[0].isdigit():
        splitted_slug[0] = str(int(splitted_slug[0]) + 1)
        return counter_separator.join(splitted_slug)
    else:
        return f"1{counter_separator}{slug}"


class Slug:
    """An alternative to Django's `django.utils.text.slugify`
    :param model_instance: Instance of `django.db.models.Model` with at least a
        `django.db.models.CharField` called `slug`.
    :param source_fields: Tuple of fields of your `model_instance` you want to use
        to fill the `slug` field. Works similar to `django.contrib.admin.ModelAdmin.prepopulated_fields`.
    :param unique_for_fields: Tuple of fields of your `model_instance` you want to use to make sure
        a `slug` is unique when used together. Works similar to `django.db.models.Model.Meta.unique_together`.
    :param slug_field_name: The name of your `slug` field, normally "slug".

    Usage

        Simple:
            slug = Slug(model_instance).get_available_slug()

        Advanced:
        `source_fields`:
            You can take advantage of `model_instance` by creating a attribute called `slug_source_fields`:
                class Article(models.Model):
                    slug_source_fields = ("title", )
            It will be used as `source_fields` automatically.


        `unique_for_fields`
            You can take advantage of `model_instance` by creating a attribute called `slug_unique_for_fields`:
                class Article(models.Model):
                    slug_unique_for_fields = ("publishing_date", )
            It will be used as `unique_for_fields` automatically.

            The usage can be as simple as a tuple of field names:
                Slug(model_instance, unique_for_fields=("publishing_date", "category"))
            Or you can provide field lookups, for example "publishing_date" could be a `DateTimeField`
            and you want to use only the "date" part of that field, you can do so by providing
            the proper lookup, like this:
                Slug(..., unique_for_fields=(("publishing_date", "publishing_date__date"), "category"))
            Attention to the detail, now our first item of `unique_for_fields` is a `tuple` containing
            (FIELD_NAME, FIELD_LOOKUP).

        `slug_field_name`
            If you have a slug field that is not called "slug", you tell `Slug` what is the name of your slug
            attribute:
                Slug(model_instance, slug_field_name="article_slug")
    """

    def __init__(
        self,
        model_instance,
        source_fields=(),
        unique_for_fields=(),
        slug_field_name="slug",
    ):
        self.source_fields = getattr(
            model_instance, "slug_source_fields", source_fields
        )
        self.unique_for_fields = getattr(
            model_instance, "slug_unique_for_fields", unique_for_fields
        )
        self.instance = model_instance
        self.original_slug = getattr(model_instance, slug_field_name)
        self._max_length = self.instance._meta.get_field(slug_field_name).max_length

    @property
    def source_field_slugs(self):
        for field_name in self.source_fields:
            yield slugify(getattr(self.instance, field_name))

    def get_available_slug(self, counter_separator="_"):
        if not self.original_slug and self.source_fields:
            # combine all fields you want to make a slug
            slug = "-".join(self.source_field_slugs)
        else:
            # This way you can manually change the `slug` field in the form
            # and here we make sure your text is properly slugified.
            slug = slugify(self.original_slug)

        # Stop here and return our `slug` in case we have no interest in
        # checking if it is unique for some field (`unique_for_fields`).
        # But if you set `unique=True` in the field definition django will
        # still validate that.
        if not self.unique_for_fields:
            return slug

        # now let's check if our `slug` is unique for fields defined in
        # `self.unique_for_fields`
        # let's start building our query:
        query = self.instance.__class__.objects.all()
        if self.instance.pk:
            # If we're already in the database we want to remove ourselves
            # from the query, otherwise we always will find some record with our slug
            # in this case we are the ones with `slug=self.slug`
            query = query.exclude(pk=self.instance.pk)

        for item in self.unique_for_fields:
            # `self.unique_for_fields` can contain field names or pairs(tuples)
            # containing field_name and a specific lookup for that field.
            # so let's unpack if we encounter a tuple
            if isinstance(item, tuple):
                field_name, lookup = item
            else:
                field_name, lookup = item, item
            query = query.filter(**{lookup: getattr(self.instance, field_name)})

        # And now, next line of code, we're going to check
        # if our slug exists, given that so far we're already filtering:
        # - any record
        # - not including ourselves
        # - and considering self.unique_for_fields, if set
        while query.filter(slug=slug).exists():
            slug = add_counter_to_slug(slug)
        # Make sure our slug doesn't exceed the `slug` `max_length`
        return slug[: self._max_length]


def slug(
    model_instance, source_fields=(), unique_for_fields=(), slug_field_name="slug"
):
    """Shortcut for using `Slug` as a simple function.
    Refer to `Slug` for more information about the parameters.
    """
    return Slug(
        model_instance, source_fields, unique_for_fields, slug_field_name
    ).get_available_slug()


# Alternative to the classic way of using a tuple of tuples for Choices in
# database fields

class Choices():
    """An alternative to the classic Choices

    Usage

        class Article(models.Model):
            STATUSES = Choices(DRAFT=_("Draft"), PUBLIC=_("Public"))

            title = models.CharField(_("Title"), max_length=140, db_index=True)
            status = models.CharField(
                max_length=10, choices=STATUSES, default=STATUSES.DRAFT, db_index=True
            )

        Comparison example:

        article = Article.objects.get(pk=1)
        # instance access:
        if article.status == article.STATUSES.PUBLIC:
            publish()

        # class access:
        Article.STATUSES.DRAFT == "DRAFT"

    - As you can see you can just do `choices=STATUSES`, that's because
        `Choices` has iterator capabilities.
    - I did some operator overloading too, so you can directly compare if
        `value == STATUSES.<STATUS>`.

    NOTE: This doesn't work if you want named groups.
    """
    def __init__(self, **kwargs):
        self.choices = kwargs

    def __iter__(self):
        return (choice for choice in self.choices.items())

    def __contains__(self, key):
        return key in self.choices

    def __getattr__(self, key):
        if key in self.choices:
            return key
        raise AttributeError(key)
