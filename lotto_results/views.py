import json

import requests
from bs4 import BeautifulSoup
from django.http import HttpRequest, HttpResponse

# from django.views import View
from django.views.generic import TemplateView


def scrape_lotto_results(url: str) -> list[dict[str, str]]:
    """
    Scrape the results of a given lotto page and returns a list
    of dictionaries with the date and numbers for each drawing.

    :param url: str: Specify the url of the website that we want to scrape
    :return: A list of dictionaries, where each dictionary has two keys:
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the data from the HTML content
    lotto_results = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) == 6:
            date = tds[0].text
            numbers = [tds[i].text for i in range(1, 6)]
            lotto_results.append({"date": date, "numbers": numbers})

    return lotto_results


class ReviewLotteryResults(TemplateView):
    template_name = "index.html"

    def get(self, request: HttpRequest, number: int) -> HttpResponse:
        """
               Checks if the number is between 2500 and 3540, returning an
               error message if it isn't. If the number is valid, it scrapes data
               from the pais website using BeautifulSoup4.

               We then checks whether any of the numbers in `lotto_results` are
               in our list of numbers (numbers). If there's a match,
               we return True for "is_winner". Otherwise we return False.

               :param request: HttpRequest: Get the request data from the client
               :param number: int: Specify the number of the lottery
               :return: A HttpResponse
        object, which is a wrapper around the
               response that django sends back to the user
        """

        if not 2500 <= number <= 3540:
            return HttpResponse(
                "Invalid number. Number must be between 2500 and 3540.", status=400
            )

        url = f"https://pais.co.il/lotto/currentlotto.aspx?lotteryId={number}"

        # scrape the data from the URL
        lotto_results = scrape_lotto_results(url)

        is_winner = any(number in lotto_results["numbers"] for _ in lotto_results)

        result = {"is_winner": is_winner}
        return HttpResponse(
            json.dumps(result),
            content_type="application/json",
        )
