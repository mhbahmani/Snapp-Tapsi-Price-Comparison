from src.twitter import Twitter
from src.grafana import Grafana
from src.telegram_handler import Telegram

from src.utils import generate_today_panel_image_file_name

import schedule
import jdatetime
import time


def report_average_panel_image():
    # twitter = Twitter()
    telegram = Telegram()
    grafana = Grafana()

    panel_image_file_path = generate_today_panel_image_file_name()
    grafana.download_panel_image(output_file_path=panel_image_file_path)

    message = f"میانگین قیمت اسنپ و تپسی در ۲۴ ساعت گذشته {jdatetime.datetime.now().strftime('%d-%m-%Y')}"
    tweet_media = [panel_image_file_path]

    # twitter.send_tweet(message, tweet_media)
    telegram.send_report(message, tweet_media)

report_average_panel_image()

schedule.every().day.at("22:00").do(report_average_panel_image)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)