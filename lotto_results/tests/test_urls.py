from django.test import TestCase
from django.urls import reverse


class TestURLPatterns(TestCase):

    """
    Test that the URL for the review lottery results view is mapped to
    the correct URL. It also checks that a GET request to this view returns
    a status code of 200 and uses the `index.html` template.
    """

    def test_review_lottery_results_view(self):
        # Set up the test data
        url = "/"
        view_name = "review-lottery-results"

        # Check that the URL maps to the correct view
        self.assertEqual(reverse(view_name), url)

        # Send a GET request to the view
        response = self.client.get(url)

        # Check the status code and the content of the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
