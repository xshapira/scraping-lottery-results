import json

import requests
from bs4 import BeautifulSoup
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


def scrape_lotto_results(url: str) -> JsonResponse:
    """
    Scrape the results of a given lotto page and returns a list
    of dictionaries with the date and numbers for each drawing.

    :param url: str: Specify the url of the website that we want to scrape
    :return: A list of dictionaries, where each dictionary has two keys:
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

        # Extract the six numbers from the `numbers` variable
        list_of_numbers = [number.text.strip() for number in numbers]
        sorted_list_of_numbers = sorted(
            list_of_numbers,
            key=lambda x: int(x),
            reverse=True,
        )

        result = {
            "title": title.text.strip().replace("\n", " "),
            "date": date.text.strip().replace("\n", " "),
            "numbers": " ".join(sorted_list_of_numbers),
            "strong_number": strong_num.text.strip().replace("\n", " "),
        }
        lotto_results.append(result)

    # Return the scraped data as a JSON response
    return JsonResponse(lotto_results, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class ReviewLotteryResults(View):
    """
    Checks if the number is between 2500 and 3540, returning an
    error message if it isn't. If the number is valid, it scrapes data
    from the pais website using BeautifulSoup4.

    We then checks whether any of the numbers in `lotto_results` are
    in our list of numbers (numbers). If there's a match,
    we return True for "is_winner". Otherwise we return False.

    :param request: HttpRequest: Get the data from the user
    :return: A json object with a single key, is_winner
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "index.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        number = request.POST.get("number")

        if not number:
            return HttpResponse("Number not provided.", status=400)
        try:
            number = int(number)
        except ValueError:
            return HttpResponse(
                "Invalid number. Number must be an integer.", status=400
            )

        if not 2500 <= number <= 3540:
            return HttpResponse(
                "Invalid number. Number must be between 2500 and 3540.", status=400
            )

        url = f"https://pais.co.il/lotto/currentlotto.aspx?lotteryId={number}"

        # Scrape the data from the URL
        lotto_results = scrape_lotto_results(url)

        # Parse the JSON data contained in the lotto_results object
        # and store it in a dictionary
        data = json.loads(lotto_results.content)

        context = {"lotto_results": data}
        return render(request, "index.html", context)
