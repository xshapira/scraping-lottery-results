import requests
from bs4 import BeautifulSoup


def scrape_lotto_results(url: str) -> list[dict[str, str]]:
    """
    Scrape the results of the lotto archive website and returns
    a list of dictionaries with the date and numbers for each drawing.

    :param url: str: Pass in the url of the website that we want to scrape
    :return: A list of dictionaries
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
