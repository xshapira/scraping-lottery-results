import uuid

from django.db import IntegrityError, models, transaction
from django.urls import reverse


class ShortUrl(models.Model):

    """ShortUrl Model Definition"""

    key = models.CharField(
        max_length=7,
        primary_key=True,
        editable=False,
        unique=True,
    )
    long_url = models.URLField(verbose_name="Long URL")
    visits = models.PositiveIntegerField(default=0, verbose_name="Visits")
    # created_at = models.DateTimeField(
    #     auto_now_add=True,
    #     verbose_name="Created At",
    # )

    # String representation of our model class instance
    def __str__(self):
        return self.key

    # Overriding the default save method of parent class to customize extra fields
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key(self.long_url)
        super().save(*args, **kwargs)

    # Updating the instance without modifying the key of current instance
    def update(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # Generating random new key for short url
    @classmethod
    def generate_key(cls, long_url: str):
        while True:
            key = uuid.uuid4().hex[:7]
            try:
                # We limit the outcome of a possible exception that can have
                # on any exterior transactions. We want to prevent
                # the error “current transaction is aborted,
                # queries ignored until end of transaction block”.
                with transaction.atomic():
                    return ShortUrl.objects.create(key=key, long_url=long_url)
            except IntegrityError:
                continue

    def get_absolute_url(self, request):
        return reverse("entry_point", kwargs={"url_key": self.key})

    def get_current_host(self, request):
        scheme = request.is_secure() and "https" or "http"
        return f"{scheme}://{request.get_host()}"

    class Meta:
        verbose_name = "Short Url"
