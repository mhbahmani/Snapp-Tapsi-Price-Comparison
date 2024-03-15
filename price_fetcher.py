from src.snapp import Snapp
from src.tapsi import Tapsi
from src.metrics_handler import MetricsHandler
from src.utils import load_routes

from decouple import config 
from jdatetime import datetime

from time import sleep
import re


SCRAPE_INTERVAL = int(config("SCRAPE_INTERVAL", 300, cast=int))

snapp = Snapp()
tapsi = Tapsi()
exporter = MetricsHandler("./prices.txt")


def fetch_prices(routes: list):
    prices = []
    # for in_hurry in [False, True]:
    for in_hurry in [False]:
        try:
            for route in routes:
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

            for route in routes:
                print("TAPSI", route["tag"], "IN_HURRY:", in_hurry)
                prices.append(
                    {
                        "provider": "tapsi",
                        "route": route["tag"],
                        "price": tapsi.get_route_price_with_discount(
                            route["source"],
                            route["destination"],
                            in_hurry=in_hurry),
                        "in_hurry": in_hurry
                    }
                )
                sleep(1)
        except Exception as e:
            print(e)
            print("Use backup server")
            break

        # Get minimum price for different routes
        pattern = re.compile(r"uni.*tapsi.*")
        min_price_uni_tapsi_dict: dict = \
            min(prices, key=lambda x: x["price"] if pattern.match(x["route"]) and x['provider'] == "tapsi" else 1000000000)
        min_price_uni_tapsi_dict = min_price_uni_tapsi_dict.copy()
        pattern = re.compile(r"home.*tapsi.*")
        min_price_home_tapsi_dict: dict = \
            min(prices, key=lambda x: x["price"] if pattern.match(x["route"]) else 1000000000)
        min_price_home_tapsi_dict = min_price_home_tapsi_dict.copy()
    else:
        metrics = exporter.parse_prices_into_metrics(prices)
        metrics += exporter.add_min_price_metric(min_price_uni_tapsi_dict, key="uni_to_tapsi")
        metrics += exporter.add_min_price_metric(min_price_home_tapsi_dict, key="home_to_tapsi")
        exporter.export_metrics(metrics)
        
    print("Done")


if __name__ == "__main__":
    routes = load_routes()

    # Set a flag to pass to code on running command in order to bypass while loop
    # and run the code once
    if config("RUN_ONCE", False, cast=bool):
        print("RUN_ONCE is set to True, running once")
        fetch_prices(routes)
        exit(0)

    print(f"Scrape Interval: {SCRAPE_INTERVAL}")

    while True:
        print(f"Fetching prices at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        fetch_prices(routes)
        sleep(SCRAPE_INTERVAL)

