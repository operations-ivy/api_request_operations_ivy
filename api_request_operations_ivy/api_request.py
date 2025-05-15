from __future__ import annotations

import json
from json.decoder import JSONDecodeError

import requests
from requests.exceptions import HTTPError
from requests.exceptions import RequestException


class ApiRequest:
    def __init__(self):
        self.base_api_url = "https://api.chucknorris.io/jokes/"

    def _get(self, endpoint: str) -> dict:
        url = self.base_api_url + endpoint
        try:
            response = requests.get(url)
            response.raise_for_status()
            return json.loads(response.text)
        except HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}", "status_code": response.status_code}
        except JSONDecodeError as json_err:
            return {"error": f"Invalid JSON response: {json_err}"}
        except RequestException as req_err:
            return {"error": f"Request error: {req_err}"}

    def get_random(self) -> dict:
        """
        Returns a random Chuck Norris joke.
        """
        return self._get("random")

    def get_random_joke_from_category(self, category: str) -> dict:
        """
        Returns a random Chuck Norris joke from the specified category.
        """
        return self._get(f"random?category={category}")

    def find_specific(self, query: str) -> dict:
        """
        Returns a list of Chuck Norris jokes that match the query.
        """
        return self._get(f"search?query={query}")

    def get_categories(self) -> list | dict:
        """
        Returns a list of all the categories of Chuck Norris jokes.
        """
        return self._get("categories")
