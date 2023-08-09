import schedule
import time


def tweet_average_panel_image():
    pass


schedule.every().day.at("22:00").do(tweet_average_panel_image)


while True:
    schedule.run_pending()
    time.sleep(15 * 60)