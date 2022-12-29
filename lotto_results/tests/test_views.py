import json

from django.conf import settings
from django.test import Client, RequestFactory, TestCase
from django.urls import resolve, reverse

from lotto_results.views import HomeView


class TestHomeView(TestCase):
    def setUp(self):
        # This method is called at the beginning of each test
        self.url = reverse("index")
        self.response = self.client.get(self.url)
        self.factory = RequestFactory()
        # ensure debug is set to False
        self.debug = settings.DEBUG
        settings.DEBUG = False

    def tearDown(self):
        # This method is called at the end of each test
        settings.DEBUG = self.debug

    def test_home_url_resolves_to_offer_view(self):
        self.assertEquals(resolve(self.url).func.view_class, HomeView)

    def test_home_view_name(self):
        # Ensure name of the view is "index"
        view = resolve(self.url)
        self.assertEqual(view.func.__name__, HomeView.as_view().__name__)

    def test_successful_home_view_get_response(self):
        # Ensure the response is 200 OK
        request = self.factory.get("")
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_home_view_returns_correct_html(self):
        # Ensure the response contains the correct html
        self.assertContains(self.response, "URL Shortener")
        self.assertNotContains(self.response, "hello world")


class TestsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("create")

    def test_short_url_POST(self):
        # Create a new short url
        url = reverse("create")
        data = {"url": "https://duckduckgo.com"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_redirect_url(self):
        url = reverse("create")
        data = {"url": "https://duckduckgo.com"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        url_key = json.loads(response.content.decode("utf-8")).get("short_url")
        response = self.client.get(url_key)
        self.assertEqual(response.status_code, 302)

    def test_redirect_url_404(self):
        # A test for a redirect url that doesn't exist in the database
        # and should return a 404
        url = reverse("create")
        data = {"url": "https://duckduckgo.com"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        url_key = json.loads(response.content.decode("utf-8")).get("short_url")
        response = self.client.get(f"{url_key}1")
        self.assertEqual(response.status_code, 404)

    def test_redirect_url_visits(self):
        # Ensure that redirect url visits are incremented
        url = reverse("create")
        data = {"url": "https://duckduckgo.com"}
        response = self.client.post(url, data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        url_key = json.loads(response.content.decode("utf-8")).get("short_url")
        response = self.client.get(url_key)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(url_key)
        self.assertEqual(response.status_code, 302)
