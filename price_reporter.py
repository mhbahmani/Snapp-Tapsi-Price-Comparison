from src.twitter_handler import Twitter
from src.grafana import Grafana
from src.telegram_handler import Telegram

from src.utils import generate_today_panel_image_file_name

import schedule
import jdatetime
import time

panels = [
    {
        "panel_id": 2,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "میانگین قیمت اسنپ و تپسی در ۲۴ ساعت گذشته {}"
    },
]


def report_average_panel_image():
    # twitter = Twitter()
    telegram = Telegram()
    grafana = Grafana()

    for panel in panels:
        panel_image_file_path = generate_today_panel_image_file_name(panel["panel_id"])
        grafana.download_panel_image(output_file_path=panel_image_file_path, panel_id=panel["panel_id"], dashboard_id=panel["dashboard_id"])

        medias = [panel_image_file_path]

        # twitter.send_tweet(panel["message"].format(jdatetime.date.today()), medias)
        telegram.send_report(panel["message"].format(jdatetime.date.today()), medias)

report_average_panel_image()

schedule.every().day.at("22:00").do(report_average_panel_image)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)