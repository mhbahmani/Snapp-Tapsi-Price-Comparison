from decouple import config
from datetime import datetime

import requests
import shutil


class Grafana:
    def __init__(self) -> None:
        self.host = config("GRAFANA_HOST")
        self.port = config("GRAFANA_PORT", "443")

        self.ORG_ID = 1

        self.TOKEN = config("GRAFANA_TOKEN")

    def download_panel_image(
            self,
            output_file_path: str,
            panel_id: int,
            dashboard_id: str,
            width: int = 1500,
            height: int = 600,
            from_date: str = "now-24h",
            to_date: str = "now"):
        request = requests.get(
            url=f"https://{self.host}:{self.port}/render/d-solo/"
                f"{dashboard_id}?from={from_date}&to={to_date}"
                f"&orgId={self.ORG_ID}&panelId={panel_id}"
                f"&width={width}&height={height}"
                f"&tz=Asia/Tehran",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
            stream=True
        )

        # print(f"Request status code: {request.status_code}")
        if request.status_code == 200:
            print(f"Start saving result to file: {output_file_path}")

            with open(output_file_path, 'wb') as image_file:
                request.raw.decode_content = True
                shutil.copyfileobj(request.raw, image_file)