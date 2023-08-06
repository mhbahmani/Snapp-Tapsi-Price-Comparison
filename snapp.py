from classes import Node

import requests
import http


class Snapp:
    RIDE_REQUEST_API = "https://app.snapp.taxi/api/api-base/v2/passenger/newprice/s/6/0"

    def __init__(self) -> None:


            
    def call_ride_request_api(self, source: Node, destination: Node, hurry_flag: bool = False) -> dict:
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

        response = requests.post(
            Snapp.RIDE_REQUEST_API,
            cookies=self.cookies,
            headers=self.headers,
            json=json_data,
        )

        if response.status_code == http.HTTPStatus.UNAUTHORIZED:
            print("Unauthorized")
            raise Exception()
        if response.status_code != http.HTTPStatus.OK:
            print(response.status_code)
            raise Exception()
        
        return response.json()

    def get_route_price(self, source: Node, destination: Node, in_hurry: bool = False) -> int:
        response = self.call_ride_request_api(source, destination, hurry_flag=in_hurry)
        for price in response.get("data", {}).get("prices"):
            if price.get("type") == "1":
                price_int = int(int(price["final"]) / 10)
                if price_int > 200000:
                    print()
                    print(price_int)
                    print(price)
                    print("////////////")
                return price_int
        raise Exception()