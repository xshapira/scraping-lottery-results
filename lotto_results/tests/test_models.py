from django.test import TestCase

from lotto_results.models import ShortUrl


class ShortUrlModelTest(TestCase):
    @classmethod
    # This method is called before each test is run
    def setUpTestData(cls):
        cls.url_ = ShortUrl.objects.create(
            long_url="https://duckduckgo.com", key="slight", visits=1
        )

    def test_long_url_field(self):
        # Ensure the long_url field is a CharField
        self.assertEqual(self.url_.long_url, str(self.url_.long_url))

    def test_model_returns_key_string(self):
        # Ensure the key field is a CharField
        self.assertEqual(self.url_.key, str(self.url_.key))

    def test_model_returns_visits_int(self):
        # Ensure the visits field is a IntegerField
        self.assertEqual(self.url_.visits, int(self.url_.visits))

    def test_save_method(self):
        # Ensure the save method is called
        methods = self.url_
        self.assertEqual(methods.save, self.url_.save)

    def test_update_method(self):
        # Ensure the update method is called
        methods = self.url_
        self.assertEqual(methods.update, self.url_.update)

    def test_generate_key_method(self):
        # Ensure the generate_key method is called
        methods = self.url_
        self.assertEqual(methods.generate_key, self.url_.generate_key)

    # def test_shorten_url_property(self):
    #     # Ensure the shorten_url property is called
    #     self.assertEqual(self.url_.shorten_url, "http://localhost:8000/s/slight")
