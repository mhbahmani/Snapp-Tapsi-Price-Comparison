class MetricsHandler:
    def __init__(self, metrics_file_path: str) -> None:
        self.metrics_file_path = metrics_file_path
        self.metrics = []

    def export_metrics(self, metrics) -> None:
        # Save self.metrics into a file
        if not metrics:
            return
        with open(self.metrics_file_path, "w") as metrics_file:
            metrics_file.write("\n".join(metrics))

    def add_min_price_metric(self, price: dict, key: str) -> None:
        metrics = []
        price["key"] = key
        value = price["price"]
        del(price["price"])
        metrics.append(
            "min_price{" + ", ".join([f"{key}=\"{price[key]}\"" for key in price]) + "} " + str(value)
        )
        return metrics

    def parse_prices_into_metrics(self, prices: list) -> list:
        # Parse data into self.metrics
        metrics = []
        for price in prices:
            value = price["price"]
            del(price["price"])
            metrics.append("price{" + ", ".join([f"{key}=\"{price[key]}\"" for key in price]) + "} " + str(value))
        return metrics