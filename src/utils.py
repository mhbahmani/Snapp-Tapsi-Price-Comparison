from jdatetime import datetime
from src.classes import Node

import json


def generate_today_panel_image_file_name(panel_id):
    return f"./panels/panel-{str(panel_id)}-{datetime.now().strftime('%Y-%m-%d')}.png"


def load_routes():
    ROUTES_JSON_FILE_PATH = "./configs/routes.json"

    print(f"Loading routes from {ROUTES_JSON_FILE_PATH}")
    routes = []
    with open(ROUTES_JSON_FILE_PATH, "r") as f:
        routes = json.load(f).get("ROUTES", [])

    for route in routes:
        route["source"] = Node(route["source"]["lat"], route["source"]["long"])
        route["destination"] = Node(route["destination"]["lat"], route["destination"]["long"])

    print(f"Loaded {len(routes)} routes")
    return routes