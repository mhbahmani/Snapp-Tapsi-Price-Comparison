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
        # self.get_bot_token()
        # self.bot_api.update_status(status="Hello World Final")

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


        cookies = {
            'dnt': '1',
            'lang': 'en',
            'kdt': 'WriYd9LsvAv7TAUJnf0D2fOucOylTyOrASWFrTaC',
            'des_opt_in': 'Y',
            'eu_cn': '1',
            'ads_prefs': '"HBISAAA="',
            'auth_multi': '"1001479650311360512:7657267f83989b46b498ff399d4682da4fb9394e"',
            'auth_token': '7f27ad61104cdfb1e23c39dff28b73e671061131',
            'guest_id': 'v1%3A169161819453350911',
            'ct0': 'ee88a37df8ba65e7a755840a93d5210b97a427e3f1cc6fe6a868cb15a1cba35612fd140a657bfce0499ef3dea37d90a9a7e7574fa0b175f9fd26c7add13ca28a09397955fec35175a0f895ce3ad62f3c',
            'twid': 'u%3D1637543250679529472',
        }

        headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.8',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            # 'cookie': 'dnt=1; lang=en; kdt=WriYd9LsvAv7TAUJnf0D2fOucOylTyOrASWFrTaC; des_opt_in=Y; eu_cn=1; ads_prefs="HBISAAA="; auth_multi="1001479650311360512:7657267f83989b46b498ff399d4682da4fb9394e"; auth_token=7f27ad61104cdfb1e23c39dff28b73e671061131; guest_id=v1%3A169161819453350911; ct0=ee88a37df8ba65e7a755840a93d5210b97a427e3f1cc6fe6a868cb15a1cba35612fd140a657bfce0499ef3dea37d90a9a7e7574fa0b175f9fd26c7add13ca28a09397955fec35175a0f895ce3ad62f3c; twid=u%3D1637543250679529472',
            'origin': 'https://twitter.com',
            'referer': 'https://twitter.com/compose/tweet',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'x-client-transaction-id': 'hkzp+lixb2huQ+UsS3AMSTXOTsSVv0zWbAeen9MzfLta7BuYljyIuG7oaetYAzIUnj4uAoYv9tU5Tmz3Ki4hYA4MXs7Mhw',
            'x-client-uuid': 'ef7c8b76-d9a1-4034-b680-8c6747df7a27',
            'x-csrf-token': 'ee88a37df8ba65e7a755840a93d5210b97a427e3f1cc6fe6a868cb15a1cba35612fd140a657bfce0499ef3dea37d90a9a7e7574fa0b175f9fd26c7add13ca28a09397955fec35175a0f895ce3ad62f3c',
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
        }

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
                callback="http://51.89.107.199:5000/callback"
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
                callback="http://51.89.107.199:5000/callback"
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