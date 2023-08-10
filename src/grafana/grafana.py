from decouple import config
from datetime import datetime

import requests
import shutil


class Grafana:
    def __init__(self) -> None:
        self.port = config("GRAFANA_PORT", "443")

        self.from_date = "now-24h"
        self.to_date = "now"
        self.ORG_ID = 1
        self.WIDTH = 1500
        self.HEIGHT = 600

        self.TOKEN = config("GRAFANA_TOKEN")

    def download_panel_image(self, output_file_path: str, panel_id: int, dashboard_id: str):
        request = requests.get(
            url=f"https://{self.host}:{self.port}/render/d-solo/"
                f"{dashboard_id}?from={self.from_date}&to={self.to_date}"
                f"&orgId={self.ORG_ID}&panelId={panel_id}"
                f"&width={self.WIDTH}&height={self.HEIGHT}"
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