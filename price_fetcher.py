from src.static_data import *
from src.snapp import Snapp
from src.tapsi import Tapsi
from src.metrics_handler import MetricsHandler

from time import sleep

import os


SCRAPE_INTERVAL = int(os.getenv("SCRAPE_INTERVAL", 300))

snapp = Snapp()
tapsi = Tapsi()
exporter = MetricsHandler("./prices.txt")

if __name__ == "__main__":
    print(f"Scrape Interval: {SCRAPE_INTERVAL}")
    
    while True:
        prices = []
        for in_hurry in [False, True]:
            try:
                for route in ROUTES:
                    print("SNAPP", route["tag"], "IN_HURRY:", in_hurry)
                    prices.append(
                        {
                            "provider": "snapp",
                            "route": route["tag"],
                            "price": snapp.get_route_price(
                                route["source"],
                                route["destination"],
                                in_hurry=in_hurry),
                            "in_hurry": in_hurry
                        }
                    )
                    sleep(1)
            except Exception as e:
                print(e)

            try:
                for route in ROUTES:
                    print("TAPSI", route["tag"], "IN_HURRY:", in_hurry)
                    prices.append(
                        {
                            "provider": "tapsi",
                            "route": route["tag"],
                            "price": tapsi.get_route_price(
                                route["source"],
                                route["destination"],
                                in_hurry=in_hurry),
                            "in_hurry": in_hurry
                        }
                    )
                    sleep(1)
            except Exception as e:
                print(e)
            
        exporter.parse_prices_into_metrics(prices)
        exporter.export_metrics()
        print("done")
        # print(prices)
        sleep(SCRAPE_INTERVAL)
