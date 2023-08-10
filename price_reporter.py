from src.twitter_handler import Twitter
from src.grafana import Grafana
from src.telegram_handler import Telegram

from src.utils import generate_today_panel_image_file_name

import schedule
import jdatetime
import time

panels = [
    {
        "panel_id": 3,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "میانگین قیمت اسنپ و تپسی در ۲۴ ساعت گذشته (سفر عادی)",
        "description": "Average panel (normal)"
    },
    {
        "panel_id": 43,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "میانگین قیمت اسنپ و تپسی در ۲۴ ساعت گذشته (عجله دارم)",
        "description": "Average panel (in hurry)"
    },
    {
        "panel_id": 54,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "بیش‌ترین و کم‌ترین اختلاف قیمت حالت عجله دارم و عجله ندارم در بین تمامی مسیرها ",
        "description": "Diff Max/Min"
    },
    {
        "panel_id": 39,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "قیمت Tapsi در مسیرهایی که تا به حال نرفته‌ام (حالت عادی)",
        "description": "Not Gone Routes tapsi normal"
    },
    {
        "panel_id": 50,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "قیمت Snapp در مسیرهایی که تا به حال نرفته‌ام (حالت عادی)",
        "description": "Not Gone Routes snapp normal"
    },
]


def report_average_panel_image():
    # twitter = Twitter()
    telegram = Telegram()
    grafana = Grafana()

    telegram.send_message(f"گزارش قیمت‌ها در ۲۴ ساعت گذشته {jdatetime.date.today()}")

    for panel in panels:
        panel_image_file_path = generate_today_panel_image_file_name(panel["panel_id"])
        grafana.download_panel_image(output_file_path=panel_image_file_path, panel_id=panel["panel_id"], dashboard_id=panel["dashboard_id"])

        medias = [panel_image_file_path]

        # twitter.send_tweet(panel["message"], medias)
        telegram.send_report(panel["message"], medias)
        time.sleep(10)

# report_average_panel_image()

# -03:30
schedule.every().day.at("17:30").do(report_average_panel_image)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)