from datetime import datetime

import requests
import shutil
import os


class Grafana:
    def __init__(self) -> None:
        self.port = os.getenv("GRAFANA_PORT", "443")

        self.DASHBOARD_UID = "d90a5e73-63d1-43d9-9f81-e776ba7e0c31"
        self.PANEL_ID = 3
        self.from_date = "now-24h"
        self.to_date = "now"
        self.ORG_ID = 1
        self.WIDTH = 1500
        self.HEIGHT = 600

        self.TOKEN = os.getenv("GRAFANA_TOKEN")

    def download_panel_image(self):
        request = requests.get(
            url=f"https://{self.host}:{self.port}/render/d-solo/"
                f"{self.DASHBOARD_UID}?from={self.from_date}&to={self.to_date}"
                f"&orgId={self.org_id}&panelId={self.PANEL_ID}"
                f"&width={self.WIDTH}&height={self.HEIGHT}"
                f"&tz=Asia/Tehran",
            headers={"Authorization": f"Bearer {self.TOKEN}"},
            stream=True
        )

        file_path = f"./panel/Average-panel-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
        print(f"Request status code: {request.status_code}")
        if request.status_code == 200:
            print(f"Start saving result to file: {file_path}")

            with open(file_path, 'wb') as image_file:
                request.raw.decode_content = True
                shutil.copyfileobj(request.raw, image_file)

            print(f"Image has been saved.")