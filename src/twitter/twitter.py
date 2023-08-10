from decouple import config
from requests_oauthlib import OAuth1Session

from time import sleep

import tweepy
import requests
import os


class Twitter:
    def __init__(self) -> None:
        self.twitter_auth_keys = {
            "consumer_key"        : config("TWITTER_CONSUMER_KEY"),
            "consumer_secret"     : config("TWITTER_CONSUMER_SECRET"),
            "access_token"        : config("TWITTER_ACCESS_TOKEN"),
            "access_token_secret" : config("TWITTER_ACCESS_TOKEN_SECRET")
        }
        self.get_bot_token()
        self.bot_api.update_status(status="Hello World Final")

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
        for media_path in medias:
            uploaded_media = api.media_upload(media_path)
            media_entities.append(
                {
                    'media_id': str(uploaded_media.media_id),
                    'tagged_users': [],
                })

        # api.update_status(status=text, media_ids=media_ids)

        # Make the request
        # oauth = OAuth1Session(
        #     self.twitter_auth_keys['consumer_key'],
        #     client_secret=self.twitter_auth_keys['consumer_secret'],
        #     resource_owner_key=self.twitter_auth_keys['access_token'],
        #     resource_owner_secret=self.twitter_auth_keys['access_token_secret']
        # )

        # # Making the request
        # response = oauth.post(
        #     "https://api.twitter.com/2/tweets",
        #     json={
        #         "text": text,
        #     },
        # )

        # if response.status_code != 201:
        #     raise Exception(
        #         "Request returned an error: {} {}".format(response.status_code, response.text)
        #     )

        # print("Response code: {}".format(response.status_code))




        json_data = {
            'variables': {
                'tweet_text': text,
                'dark_request': False,
                'media': {
                    'media_entities': media_entities,
                    'possibly_sensitive': False,
                },
                'semantic_annotation_ids': [],
            },
            'features': {
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'responsive_web_twitter_article_tweet_consumption_enabled': False,
                'tweet_awards_web_tipping_enabled': False,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                'responsive_web_media_download_video_enabled': False,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_enhance_cards_enabled': False,
            },
            'queryId': 'SoVnbfCycZ7fERGCwpZkYA',
        }

        response = requests.post(
            'https://twitter.com/i/api/graphql/SoVnbfCycZ7fERGCwpZkYA/CreateTweet',
            cookies=cookies,
            headers=headers,
            json=json_data,
        )


    def get_bot_token(self):
        # if token file exists, load tokens from it
        tokens_file_path = "bot_tokens.txt"
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
        auth = tweepy.OAuth1UserHandler(
            config("TWITTER_CONSUMER_KEY"), config("TWITTER_CONSUMER_SECRET"),
            access_token, access_token_secret
        )
        self.bot_api = tweepy.API(auth)

    def save_bot_tokens(self, access_token: str, access_token_secret: str):
        tokens_file_path = "bot_tokens.txt"
        with open(tokens_file_path, "w") as f:
            f.write(f"{access_token} {access_token_secret}")
    
twitter = Twitter()