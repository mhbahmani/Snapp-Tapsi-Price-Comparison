from src.twitter import Twitter
from src.grafana import Grafana
from src.utils import generate_today_panel_image_file_name

import schedule
import jdatetime
import time


def tweet_average_panel_image():
    twitter = Twitter()
    grafana = Grafana()

    panel_image_file_path = generate_today_panel_image_file_name()
    grafana.download_panel_image(output_file_path=panel_image_file_path)

    tweet_text = f"میانگین قیمت اسنپ و تپسی در ۲۴ ساعت گذشته {jdatetime.datetime.now().strftime('%Y-%m-%d')}"
    tweet_media = [panel_image_file_path]

    twitter.send_tweet(tweet_text, tweet_media)

schedule.every().day.at("22:00").do(tweet_average_panel_image)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)