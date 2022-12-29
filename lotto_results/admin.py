from django.contrib import admin

from .models import ShortUrl


@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    ordering = ("-visits",)
    list_display = (
        "__str__",
        # "created_at",
        "visits",
    )
