import json

import requests
from bs4 import BeautifulSoup
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from lotto_results.forms import LotteryResultsForm


def scrape_lotto_results(url: str) -> JsonResponse:
    """
    Accept a URL as an argument and return a JSON response containing
    the scraped data. We use BeautifulSoup to parse out the desired HTML
    content from that page.

    It then extracts the result of the lotto numbers, sorts them in
    descending order, and joins them into one string with spaces between
    each number.

    :param url: str: Pass the url of the website to be scraped
    :return: A json response
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the data from the HTML content
    main_title = soup.find_all(class_="archive_open_title lotto")
    dates = soup.find_all(class_="archive_open_dates w-clearfix")
    numbers = soup.find_all("li", class_="loto_info_num")
    strong_number = soup.find_all(class_="loto_info_num strong")

    lotto_results = []
    for title, date, strong_num in zip(main_title, dates, strong_number):

        # Extract the six lottery numbers as individual `li` elements
        # from the `numbers` variable
        list_of_numbers = [number.extract() for number in numbers]
        sorted_list_of_numbers = sorted(
            list_of_numbers,
            # Extract the text from the `Tag` object
            key=lambda x: int(x.text),
            reverse=True,
        )

        result = {
            "title": title.text.strip().replace("\n", " "),
            "date": date.text.strip().replace("\n", " "),
            "numbers": [number.text for number in sorted_list_of_numbers],
            "strong_number": strong_num.text.strip().replace("\n", " "),
        }
        lotto_results.append(result)

    # Return the scraped data as a JSON response
    return JsonResponse(lotto_results, safe=False)


class ReviewLotteryResults(View):
    """
    Checks if the number is between 2500 and 3540, returning an
    error message if it isn't. If the number is valid, it scrapes data
    from the pais website using BeautifulSoup4.

    We then checks whether any of the numbers in `lotto_results` are
    in our list of numbers (numbers). If there's a match,
    we return the winning numbers.

    :param request: HttpRequest: Get the data from the user
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        form = LotteryResultsForm()
        context = {"form": form}
        return render(request, "index.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LotteryResultsForm(request.POST)
        if not form.is_valid():
            # Form is invalid => render the template with the form instance
            return render(request, "index.html", {"form": form})
        # Process the data if Form is valid
        number = form.cleaned_data.get("number")

        url = f"https://pais.co.il/lotto/currentlotto.aspx?lotteryId={number}"

        # Scrape the data from the URL
        lotto_results = scrape_lotto_results(url)

        # Parse the JSON data contained in the lotto_results object
        # and store it in a dictionary
        data = json.loads(lotto_results.content)

        context = {"lotto_results": data, "number": number}
        return render(request, "index.html", context)
