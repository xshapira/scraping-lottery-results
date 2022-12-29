import json

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from .models import ShortUrl


class HomeView(TemplateView):
    template_name = "index.html"


# Exempting the class from csrf to avoid csrf validation error
@method_decorator(csrf_exempt, name="dispatch")
class ShortUrlView(View):

    """Calling post function that takes json data, parse it,
    and creates a new entry in ShortUrl model. It saves and returns
    a json serialized dictionary."""

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        long_url = str(data.get("url"))
        url = ShortUrl()
        url.long_url = long_url
        url.save()

        current_host = url.get_current_host(request)
        url_key = url.get_absolute_url("url_key")

        data = {
            "success": True,
            "short_url": f"{current_host}{url_key}",
            "url": long_url,
        }
        return JsonResponse(data, status=201)


# Make a view only accept GET request method
@require_http_methods(["GET"])
def redirect_to_url(request, url_key: str):

    """This function is called in each new short url call
    and updates the visits of that particular short url."""

    url = get_object_or_404(ShortUrl, key=url_key)
    url.visits = F("visits") + 1
    url.save(update_fields=["visits"])
    return redirect(url.long_url)
