import requests
from bs4 import BeautifulSoup
from django.views import View


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


class ReviewLotteryResults(View):
    pass
