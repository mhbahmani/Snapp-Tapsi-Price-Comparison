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
    # {
    #     "panel_id": 55,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "ناهار دادن به کارمندان",
    #     "description": "Lunch"
    # }
]

quick_report_pannels = [
    {
        "panel_id": 76,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "ارزان‌ترین مسیر از خانه به تپسی",
        "description": "Min Prices"
    },
    {
        "panel_id": 77,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "ارزان‌ترین‌ از خانه به دانشگاه",
        "description": "Min Prices"
    },
    {
        "panel_id": 78,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "ارزان‌ترین مسیر از دانشگاه به تپسی",
        "description": "Min Prices"
    }
]

def report_panels(quick: bool = False):
    # twitter = Twitter()
    telegram = Telegram()
    grafana = Grafana()

    if quick:
        telegram.send_message(f"🔔 گزارش لحظه‌ای \n{(jdatetime.datetime.now() + jdatetime.timedelta(hours=3, minutes=30)).strftime('%Y-%m-%d %H:%M:%S')}")
        panels = quick_report_pannels
        from_date = "now-1m"
        width = "1000"
        height = "400"
    else:
        telegram.send_message(f"📊🚖📈 گزارش قیمت‌ها در ۲۴ ساعت گذشته \n{jdatetime.date.today().strftime('%Y-%m-%d')}")
        panels = daily_report_panels
        from_date = "now-24h"
        width = "1500"
        height = "600"
    
    for panel in panels:
        panel_image_file_path = generate_today_panel_image_file_name(panel["panel_id"])
        grafana.download_panel_image(
            output_file_path=panel_image_file_path,
            panel_id=panel["panel_id"],
            dashboard_id=panel["dashboard_id"],
            width=width,
            height=height,
            from_date=from_date)

        medias = [panel_image_file_path]

        # twitter.send_tweet(panel["message"], medias)
        telegram.send_report(panel["message"], medias)
        time.sleep(10)

    print(f"////////////// {'Quick' if quick else 'Daily'} Report has been sent //////////////")

# report_panels()
report_panels(quick=True)

# -03:30
schedule.every().day.at("10:30").do(report_panels)
schedule.every().day.at("16:30").do(report_panels)
schedule.every(30).minutes.do(report_panels, quick=True)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)
