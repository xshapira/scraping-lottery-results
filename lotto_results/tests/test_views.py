from django.test import TestCase
from django.urls import reverse

from lotto_results.views import scrape_lotto_results


class TestScrapeLottoResults(TestCase):

    """
    Test the scrape_lotto_results function.
    It calls the scrape_lotto_results function with a desired URL,
    and verifies that it returns a 200 response code.
    It also verifies that the response is in JSON format.
    """

    def test_scrape_lotto_results(self):
        # Call the `scrape_lotto_results` function with the desired URL
        url = "https://pais.co.il/lotto/currentlotto.aspx?lotteryId=3540"
        response = scrape_lotto_results(url)

        self.assertEqual(response.status_code, 200)

        # Verify that the response is a JSON response
        self.assertEqual(response["Content-Type"], "application/json")


class TestReviewLotteryResults(TestCase):

    """
    Test the review_lottery_results view.
    It sends a POST request to the view with a valid number and verifies
    that the response is successful. It then sends a POST request to
    the view with an invalid number and verifies that the response
    is successful, but contains an error message.
    """

    def test_review_lottery_results(self):
        # Send a POST request to the `review_lottery_results` view
        # with a valid number
        url = reverse("review-lottery-results")
        data = {"number": 3540}
        response = self.client.post(url, data)

        # Verify that the response is a successful HTTP response
        self.assertEqual(response.status_code, 200)

        # Send a POST request to the `review_lottery_results` view
        # with an invalid number
        data = {"number": 0}
        response = self.client.post(url, data)

        # Verify that the response is a successful HTTP response
        # with the expected error message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "מספר לא תקין. המספר חייב להיות בין 2500 ל-3540.")
