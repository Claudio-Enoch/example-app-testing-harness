import os

import dotenv
import requests

from requests import Response

from hash_api.helper import timer

dotenv.load_dotenv(override=True)


class HashApi:

    def __init__(self):
        port = os.environ.get("PORT")
        self._base_url = f"http://127.0.0.1:{port}"

    def post_hash(self, body: dict) -> Response:
        response = requests.post(f"{self._base_url}/hash", json=body)
        return response

    def get_hash(self, _id) -> Response:
        response = requests.get(f"{self._base_url}/hash/{_id}")
        return response

    def get_stats(self) -> Response:
        response = requests.get(f"{self._base_url}/stats")
        return response

    def post_shutdown(self) -> Response:
        response = requests.post(f"{self._base_url}/hash")
        return response
