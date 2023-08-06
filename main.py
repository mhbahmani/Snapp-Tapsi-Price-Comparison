from static_data import *
from snapp import Snapp
from tapsi import Tapsi
from exporter import Exporter

from time import sleep

import os


SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", 300))

snapp = Snapp()
tapsi = Tapsi()
exporter = Exporter("./prices.txt")

if __name__ == "__main__":
    print(f"Scrape Interval: {SCRAPE_INTERVAL}")
    
    while True:
        prices = []
        try:
            for route in ROUTES:
                prices.append(
                    {
                        "provider": "snapp",
                        "route": route["tag"],
                        "price": snapp.get_route_price(
                            route["source"],
                            route["destination"],
                            in_hurry=False),
                         "in_hurry": False
                    }
                )
        except Exception as e:
            print(e)

        try:
            for route in ROUTES:
                prices.append(
                    {
                        "provider": "tapsi",
                        "route": route["tag"],
                        "price": tapsi.get_route_price(
                            route["source"],
                            route["destination"],
                            in_hurry=False),
                        "in_hurry": False
                    }
                )
        except Exception as e:
            print(e)

        exporter.parse_prices_into_metrics(prices)
        exporter.export_metrics()
        print("done")
        # print(prices)
        sleep(SCRAPE_INTERVAL)
