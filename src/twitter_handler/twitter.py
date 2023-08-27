# from requests_oauthlib import OAuth1Session
from decouple import config
from time import sleep

from src.utils import load_provider_headers_and_cookies

import tweepy
# import requests
import os


class Twitter:
    CONFIG_JSON_FILE_PATH = "./configs/twitter.json"

    def __init__(self) -> None:
        self.twitter_auth_keys = {
            "consumer_key"        : config("TWITTER_CONSUMER_KEY"),
            "consumer_secret"     : config("TWITTER_CONSUMER_SECRET"),
            "access_token"        : config("TWITTER_ACCESS_TOKEN"),
            "access_token_secret" : config("TWITTER_ACCESS_TOKEN_SECRET")
        }
        self.get_bot_token()

        self.headers, self.cookies = load_provider_headers_and_cookies(self.CONFIG_JSON_FILE_PATH)

    def send_tweet(self, text: str, medias: list) -> None:

        auth = tweepy.OAuthHandler(
                self.twitter_auth_keys['consumer_key'],
                self.twitter_auth_keys['consumer_secret']
                )
        auth.set_access_token(
                self.twitter_auth_keys['access_token'],
                self.twitter_auth_keys['access_token_secret']
                )
        api = tweepy.API(auth)
    
        # Upload image
        media_entities = []
        media_ids = []
        for media_path in medias:
            uploaded_media = api.media_upload(media_path)
            media_ids.append(uploaded_media.media_id)
            media_entities.append(
                {
                    'media_id': str(uploaded_media.media_id),
                    'tagged_users': [],
                })

        self.client.create_tweet(text=text, media_ids=media_ids)

    def get_bot_token(self):
        # Getting user access token in order to 
        # tweet on behalf of that user

        # if token file exists, load tokens from it
        tokens_file_path = "./configs/bot_tokens.txt"
        tokens = None
        if os.path.exists(tokens_file_path):
            with open(tokens_file_path, "r") as f:
                tokens = f.read()
        if tokens: 
            access_token, access_token_secret = tokens.split()
        else:
            oauth1_user_handler = tweepy.OAuth1UserHandler(
                config("TWITTER_CONSUMER_KEY"),
                config("TWITTER_CONSUMER_SECRET"),
                config("TWITTER_ACCESS_TOKEN"),
                config("TWITTER_ACCESS_TOKEN_SECRET"),
                callback=config("TWITTER_CALLBACK")
            )
            print(oauth1_user_handler.get_authorization_url())
            # check if tokens file is exists
            # if not, wait for 1 second
            # if tokens file exists, read it and return the tokens
            tokens_file_path = "oauth_tokens.txt"
            while True:
                if os.path.exists(tokens_file_path):
                    with open(tokens_file_path, "r") as f:
                        tokens = f.read()
                    if tokens:
                        break
                sleep(2)
            os.remove(tokens_file_path)
            oauth_token, oauth_verifier = tokens.split(" ")

            request_token = oauth1_user_handler.request_token["oauth_token"]
            request_secret = oauth1_user_handler.request_token["oauth_token_secret"]
            print(request_secret, request_token)

            new_oauth1_user_handler = tweepy.OAuth1UserHandler(
                request_token, request_secret,
                callback=config("TWITTER_CALLBACK")
            )
            new_oauth1_user_handler.request_token = {
                "oauth_token": oauth_token,
                "oauth_token_secret": request_secret
            }
            access_token, access_token_secret = (
                new_oauth1_user_handler.get_access_token(
                    oauth_verifier
                )
            )

        self.save_bot_tokens(access_token, access_token_secret)
        self.client = tweepy.Client(
            consumer_key=config("TWITTER_CONSUMER_KEY"),
            consumer_secret=config("TWITTER_CONSUMER_SECRET"),
            access_token=access_token,
            access_token_secret=access_token_secret
        )

    def save_bot_tokens(self, access_token: str, access_token_secret: str):
        tokens_file_path = "bot_tokens.txt"
        with open(tokens_file_path, "w") as f:
            f.write(f"{access_token} {access_token_secret}")
    
twitter = Twitter()