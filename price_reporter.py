from src.twitter_handler import Twitter
from src.grafana import Grafana
from src.telegram_handler import Telegram

from src.utils import generate_today_panel_image_file_name

import schedule
import jdatetime
import time

panels = [
    # {
    #     "panel_id": 3,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "میانگین قیمت اسنپ و تپسی در ۲۴ ساعت گذشته (سفر عادی)",
    #     "description": "Average panel (normal)"
    # },
    # {
    #     "panel_id": 43,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "میانگین قیمت اسنپ و تپسی در ۲۴ ساعت گذشته (عجله دارم)",
    #     "description": "Average panel (in hurry)"
    # },
    # {
    #     "panel_id": 44,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "میانگین اختلاف قیمت حالت عادی و حالت عجله دارم",
    #     "description": "In Hurry and Normal Price Diff Average"
    # },
    # {
    #     "panel_id": 54,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "بیش‌ترین و کم‌ترین اختلاف قیمت حالت عجله دارم و عجله ندارم در بین تمامی مسیرها ",
    #     "description": "Diff Max/Min"
    # },
    # {
    #     "panel_id": 39,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "قیمت Tapsi در مسیرهایی که تا به حال نرفته‌ام (حالت عادی)",
    #     "description": "Not Gone Routes tapsi normal"
    # },
    # {
    #     "panel_id": 50,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "قیمت Snapp در مسیرهایی که تا به حال نرفته‌ام (حالت عادی)",
    #     "description": "Not Gone Routes snapp normal"
    # },
    # {
    #     "panel_id": 51,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "مشتق میانگین قیمت تپسی در مسیر‌هایی که تا به حال نرفته‌ام در ۲۴ ساعت گذشته",
    #     "description": "Tapsi Not Gone Routes Deviation 24h"
    # },
    # {
    #     "panel_id": 56,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "مشتق میانگین قیمت تپسی در مسیر‌هایی که تا به حال نرفته‌ام در هفت روز گذشته",
    #     "description": "Tapsi Not Gone Routes Deviation 7d"
    # },
    # {
    #     "panel_id": 42,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "مشتق میانگین قیمت اسنپ در مسیر‌هایی که تا به حال نرفته‌ام در ۲۴ ساعت گذشته",
    #     "description": "Snapp Not Gone Routes Deviation 24h"
    # },
    # {
    #     "panel_id": 57,
    #     "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
    #     "message": "مشتق میانگین قیمت اسنپ در مسیر‌هایی که تا به حال نرفته‌ام در هفت روز گذشته",
    #     "description": "Snapp Not Gone Routes Deviation 7d"
    # }
    {
        "panel_id": 61,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "(در حالت عادی) میانگین اختلاف قیمت مسیر از خونه تا در تپسی و از خونه تا جلوی بیمارستان مدرس",
        "description": "Home-Tapsi (Modarres and Tapsi) Average Difference (Normal)"
    },
    {
        "panel_id": 62,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "(در حالت عادی) میانگین اختلاف قیمت مسیر از دانشگاه (در آزادی) تا در تپسی و از دانشگاه (در آزادی) تا جلوی بیمارستان مدرس",
        "description": "Uni/Azadi-Tapsi (Modarres and Tapsi) Average Difference (Normal)"
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
        "panel_id": 58,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "(در حالت عادی) قیمت اسنپ در مسیر از خونه تا در تپسی و از خونه تا جلوی بیمارستان مدرس و از خونه تا سر کوچه ارغوان",
        "description": "Home-Tapsi (Snapp)"
    },
    {
        "panel_id": 55,
        "dashboard_id": "d90a5e73-63d1-43d9-9f81-e776ba7e0c31",
        "message": "ناهار دادن به کارمندان",
        "description": "Lunch"
    }
]


def report_average_panel_image():
    # twitter = Twitter()
    telegram = Telegram()
    grafana = Grafana()

    telegram.send_message(f"📊🚖📈 گزارش قیمت‌ها در ۲۴ ساعت گذشته \n{jdatetime.date.today().strftime('%Y-%m-%d')}")

    for panel in panels:
        panel_image_file_path = generate_today_panel_image_file_name(panel["panel_id"])
        grafana.download_panel_image(output_file_path=panel_image_file_path, panel_id=panel["panel_id"], dashboard_id=panel["dashboard_id"])

        medias = [panel_image_file_path]

        # twitter.send_tweet(panel["message"], medias)
        telegram.send_report(panel["message"], medias)
        time.sleep(10)

    print("////////////// Report has been sent //////////////")

report_average_panel_image()

# -03:30
schedule.every().day.at("10:30").do(report_average_panel_image)
schedule.every().day.at("16:30").do(report_average_panel_image)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)
