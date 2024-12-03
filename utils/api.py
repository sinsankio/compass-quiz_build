from enum import Enum
from typing import Any

import requests


class HttpMethod(Enum):
    GET = 0,
    POST = 1,
    PUT = 2,
    DELETE = 3


def perform_request(request: HttpMethod, url: str, data: dict = None, params: dict = None) -> Any | None:
    if request == HttpMethod.GET:
        response = requests.get(url, params=params)
    elif request == HttpMethod.POST:
        response = requests.post(url, params=params, json=data)
    elif request == HttpMethod.PUT:
        response = requests.put(url, params=params, json=data)
    else:
        response = requests.delete(url, params=params, json=data)
    if response.status_code == 200:
        return response.json()
