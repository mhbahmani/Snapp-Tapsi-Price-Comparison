from src.classes import Node
from src.utils import load_provider_headers_and_cookies

from time import sleep

import requests
import http


class Tapsi:
    CONFIG_FILE_PATH = "./configs/tapsi.json"
    RIDE_REQUEST_API = "https://api.tapsi.cab/api/v2.4/ride/preview"
    REFRESH_ACCESS_TOKEN_API = "https://api.tapsi.cab/api/v2/user/accessToken/web"
    NUM_OF_RETRY = 3

    def __init__(self) -> None:
        self.headers, self.cookies = load_provider_headers_and_cookies(Tapsi.CONFIG_FILE_PATH)

    def call_ride_request_api(self, source: Node, destination: Node) -> dict:
        json_data = {
            'origin': {
                'latitude': float(source.lat),
                'longitude': float(source.long),
            },
            'destinations': [
                {
                    'latitude': float(destination.lat),
                    'longitude': float(destination.long),
                },
            ],
            'hasReturn': False,
            'waitingTime': 0,
            'gateway': 'CAB',
            'initiatedVia': 'WEB',
        }

        for _ in range(Tapsi.NUM_OF_RETRY):
            try:
                response = requests.post(Tapsi.RIDE_REQUEST_API, cookies=self.cookies, headers=self.headers, json=json_data, timeout=5)
                break
            except requests.exceptions.ConnectTimeout:
                print("Timeout, Waiting...")
                sleep(10)

        if response.status_code == http.HTTPStatus.UNAUTHORIZED:
            print("Unauthorized")
            print("Update access token")
            self.refresh_access_token()
            print("Retry")
            response = requests.post(Tapsi.RIDE_REQUEST_API, cookies=self.cookies, headers=self.headers, json=json_data)
        if response.status_code != http.HTTPStatus.OK:
            print(response.status_code)
            raise Exception()
        
        return response.json()


    def get_route_price(self, source: Node, destination: Node, in_hurry: bool = False) -> int:
        desired_category = "STANDARD" if not in_hurry else "PRIORITY"
        
        response = self.call_ride_request_api(source, destination)

        for category in response.get("data", {}).get("categories", []):
            if category.get("key") == "NORMAL":
                for service in category.get("services"):
                    if service.get("key") == desired_category:
                        return \
                            int(service.get("prices")[0].get("passengerShare")) + \
                            int(service.get("prices")[0].get("discount"))


    def refresh_access_token(self):
        response = requests.get(Tapsi.REFRESH_ACCESS_TOKEN_API, cookies=self.cookies, headers=self.headers)
        self.cookies = self.retrieve_set_cookie_headers_from_response(response)

    def retrieve_set_cookie_headers_from_response(self, response: requests.Response) -> dict:
        """
            output:
            {
                'accessToken': str
                'refreshToken' srt
            }
        """

        set_cookie_headers = response.headers.get("Set-Cookie", "")
        set_cookie_headers = set_cookie_headers.split(";")

        cookies = {}
        for header in set_cookie_headers:
            header = header.split(",")
            for h in header:
                h = h.strip()
                if h.startswith("accessToken="):
                    cookies["accessToken"] = h[len("accessToken="):]
                elif h.startswith("refreshToken="):
                    cookies["refreshToken"] = h[len("refreshToken="):]

        return cookies