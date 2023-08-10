from decouple import config

import telegram
import datetime


class Telegram:
    def __init__(self) -> None:
        self.CHANNEL_NAME = "Snapp/Tapsi Price Comparison"
        self.CHANNEL_ID = -1001945780088

        self.bot = telegram.Bot(
            token=config("TELEGRAM_BOT_TOKEN")
        )

    def send_report(self, text: str, medias: list):
        self.bot.send_media_group(
            chat_id=self.CHANNEL_ID,
            media=[
                telegram.InputMediaPhoto(
                    media=open(media_path, 'rb'),
                    caption=text if i == 0 else None,
                )
                for i, media_path in enumerate(medias)
            ],
        )
        print(f"Report has been sent at {datetime.datetime.now()}")
    
    def send_message(self, text: str):
        self.bot.send_message(
            chat_id=self.CHANNEL_ID,
            text=text,
        )
        print(f"Message has been sent at {datetime.datetime.now()}")