from src.twitter_handler import Twitter
from src.grafana import Grafana
from src.telegram_handler import Telegram

from src.utils import generate_today_panel_image_file_name

import schedule
import jdatetime
import time

daily_report_panels = [
    {
        "panel_id": 61,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "(در حالت عادی) میانگین اختلاف قیمت مسیر از خونه تا در تپسی و از خونه تا جلوی بیمارستان مدرس",
        "description": "Home-Tapsi (Modarres and Tapsi) Average Difference (Normal)"
    },
    {
        "panel_id": 63,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "(در حالت عادی) میانگین اختلاف قیمت مسیر از دانشگاه (در انرژی) تا در تپسی و از دانشگاه (در انرژی) تا جلوی بیمارستان مدرس",
        "description": "Uni/Energy-Tapsi (Modarres and Tapsi) Average Difference (Normal)"
    },
    {
        "panel_id": 60,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "(در حالت عادی) قیمت تپسی در مسیر از خونه تا در تپسی و از خونه تا جلوی بیمارستان مدرس و از خونه تا سر کوچه ارغوان",
        "description": "Home-Tapsi (Tapsi)"
    },
    {
        "panel_id": 55,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "ناهار دادن به کارمندان",
        "description": "Lunch"
    }
]

quick_report_pannels = [
    {
        "panel_id": 69,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "کم‌قیمت‌ترین مسیرها",
        "description": "Min Prices"
    },
]

def report_panels(quick: bool = False):
    # twitter = Twitter()
    telegram = Telegram()
    grafana = Grafana()

    if quick:
        telegram.send_message(f"🔔 گزارش لحظه‌ای \n{jdatetime.date.today().strftime('%Y-%m-%d')}")
        panels = quick_report_pannels
    else:
        telegram.send_message(f"📊🚖📈 گزارش قیمت‌ها در ۲۴ ساعت گذشته \n{jdatetime.date.today().strftime('%Y-%m-%d')}")
        panels = daily_report_panels
    
    for panel in panels:
        panel_image_file_path = generate_today_panel_image_file_name(panel["panel_id"])
        grafana.download_panel_image(output_file_path=panel_image_file_path, panel_id=panel["panel_id"], dashboard_id=panel["dashboard_id"])

        medias = [panel_image_file_path]

        # twitter.send_tweet(panel["message"], medias)
        telegram.send_report(panel["message"], medias)
        time.sleep(10)

    print("////////////// Report has been sent //////////////")

report_panels()
report_panels(quick=True)

# -03:30
schedule.every().day.at("10:30").do(report_panels)
schedule.every().day.at("16:30").do(report_panels)
schedule.every(30).minutes.do(report_panels, quick=True)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)
