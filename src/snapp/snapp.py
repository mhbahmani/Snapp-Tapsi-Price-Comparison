from src.classes import Node
from src.utils import load_provider_headers_and_cookies, update_config_file

import requests
import http


class Snapp:
    CONFIG_FILE_PATH = "./configs/snapp.json"
    RIDE_REQUEST_API = "https://app.snapp.taxi/api/api-base/v2/passenger/newprice/s/6/0"
    AUTH_API = "https://app.snapp.taxi/api/api-passenger-oauth/v1/auth"
    NUM_OF_RETRY = 3

    def __init__(self) -> None:
        self.headers, self.cookies, self.access_token, self.refresh_token, self.auth_json_data = \
            load_provider_headers_and_cookies(Snapp.CONFIG_FILE_PATH, keys=["headers", "cookies", "access_token", "refresh_token", "auth_json_data"])

    def call_ride_request_api(self, source: Node, destination: Node, hurry_flag: bool = False, authorization_retry: bool = False) -> dict:
        json_data = {
            'points': [
                {
                    'lat': source.lat,
                    'lng': source.long,
                },
                {
                    'lat': destination.lat,
                    'lng': destination.long,
                },
                None,
            ],
            'waiting': None,
            'round_trip': False,
            'voucher_code': None,
            'service_types': [
                1,
                2,
            ],
            'hurry_price': 0 if not hurry_flag else -1,
            'hurry_flag': None if not hurry_flag else 1,
            'priceriderecom': False,
            'tag': 0,
        }

        # Send post request with timeout and retry if failed
        response = None
        for _ in range(Snapp.NUM_OF_RETRY):
            try:
                response = requests.post(
                    Snapp.RIDE_REQUEST_API,
                    # cookies=self.cookies,
                    headers=self.headers,
                    json=json_data,
                    timeout=5,
                )
                break
            except Exception as e:
                print(e)
                print("Retrying...")
                continue
        else:
            print("Failed to send request")
            raise Exception()

        if response.status_code == http.HTTPStatus.UNAUTHORIZED and not authorization_retry:
            print("Unauthorized")
            self.refresh_access_token()
            print("Retrying...")
            return self.call_ride_request_api(source, destination, hurry_flag, authorization_retry=True)
        if response.status_code != http.HTTPStatus.OK:
            print(response.status_code)
            raise Exception()
        
        return response.json()

    def get_route_price(self, source: Node, destination: Node, in_hurry: bool = False) -> int:
        response = self.call_ride_request_api(source, destination, hurry_flag=in_hurry)
        for price in response.get("data", {}).get("prices"):
            if price.get("type") == "1":
                return int(int(price["final"]) / 10)
        raise Exception()
    
    # Each 14 days, token gets expired and we need to refresh it
    def refresh_access_token(self) -> None:
        # Add refresh token to json data
        self.auth_json_data["refresh_token"] = self.refresh_token

        response = requests.post(
            Snapp.AUTH_API,
            headers=self.headers,
            json=self.auth_json_data,
        )

        if response.status_code != http.HTTPStatus.OK:
            print(response.status_code)
            raise Exception()
        
        self.refresh_token = response.json().get("refresh_token")
        self.access_token = response.json().get("access_token")

        # Update tokens in config/snap.json
        update_config_file(
            Snapp.CONFIG_FILE_PATH,
            {
                "access_token": self.access_token,
                "refresh_token": self.refresh_token
            }
        )

        # Update headers
        self.headers["authorization"] = f"Bearer {self.access_token}"

        # Update headers in config/snap.json
        update_config_file(
            Snapp.CONFIG_FILE_PATH,
            {"headers": self.headers}
        )
