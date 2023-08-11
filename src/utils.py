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

def load_provider_headers_and_cookies(file_path, keys=["headers", "cookies"]):
    with open(file_path, "r") as f:
        config = json.load(f)
    return [config[key] for key in keys]

def update_config_file(file_path, new_key_valeus: dict):
    with open(file_path, "r") as f:
        config = json.load(f)
    
    try:
        for key, value in new_key_valeus.items():
            config[key] = value
    except KeyError:
        print("Invalid key")
        return
    
    with open(file_path, "w") as f:
        json.dump(config, f, indent=4)
