class MetricsHandler:
    def __init__(self, metrics_file_path: str) -> None:
        self.metrics_file_path = metrics_file_path
        self.metrics = {}

    def export_metrics(self) -> None:
        # Save self.metrics into a file
        if not self.metrics:
            return
        with open(self.metrics_file_path, "w") as metrics_file:
            metrics_file.write("\n".join(self.metrics))

    def parse_prices_into_metrics(self, prices: list) -> list:
        # Parse data into self.metrics
        self.metrics = []
        for price in prices:
            value = price["price"]
            del(price["price"])
            self.metrics.append("price{" + ", ".join([f"{key}=\"{price[key]}\"" for key in price]) + "} " + str(value))
