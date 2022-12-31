from django.apps import apps
from django.test import TestCase

from lotto_results.apps import LottoResultsConfig


class TestAppConfig(TestCase):
    """
    Test whether the app is installed and if it's name matches what we expect.
    It also checks that the app has been registered with Django.

    :return: The name of the app and the name of the appconfig class
    """

    def test_app(self):
        self.assertEqual("lotto_results", LottoResultsConfig.name)
        self.assertEqual("lotto_results", apps.get_app_config("lotto_results").name)
