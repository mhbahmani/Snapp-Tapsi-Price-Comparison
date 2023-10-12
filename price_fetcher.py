from src.snapp import Snapp
from src.tapsi import Tapsi
from src.metrics_handler import MetricsHandler
from src.utils import load_routes

from decouple import config 
from jdatetime import datetime

from time import sleep


SCRAPE_INTERVAL = int(config("SCRAPE_INTERVAL", 300, cast=int))

snapp = Snapp()
tapsi = Tapsi()
exporter = MetricsHandler("./prices.txt")


def fetch_prices(routes: list):
    prices = []
    for in_hurry in [False, True]:
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
            print("Use backup server")
            break
    else:
        exporter.parse_prices_into_metrics(prices)
        exporter.export_metrics()
        
    print("Done")
    # print(prices)


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

