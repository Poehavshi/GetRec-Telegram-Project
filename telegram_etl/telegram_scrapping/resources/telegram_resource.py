from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup
from dagster import ConfigurableResource
from tqdm import tqdm

from telegram_scrapping.resources.html_parser import TelegramHTMLParser
from telegram_scrapping.schemas.telegram_post import TelegramPost

TELEGRAM_POST_BASE_URL = "https://t.me"


class TelegramClient(ConfigurableResource, ABC):
    @abstractmethod
    def fetch_post(self, post_id: int, channel_name: str) -> TelegramPost | None:
        pass

    @abstractmethod
    def fetch_posts_from_channel(self, channel_name: str) -> list[TelegramPost]:
        pass


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/77.0.3865.90 Safari/537.36 TelegramBot (like TwitterBot)"
}
html_parser = TelegramHTMLParser()


class TelegramRequestsClient(TelegramClient):
    def fetch_post(self, post_id: int, channel_name: str) -> TelegramPost | None:
        post_url = f"{TELEGRAM_POST_BASE_URL}/{channel_name}/{post_id}?embed=1&mode=tme"
        try:
            html_response = self._request_html(post_url)
            post = html_parser.parse_one_post(html_response)
        except requests.exceptions.RequestException:
            return None
        except AttributeError:
            return None
        return post

    def fetch_posts_from_channel(self, channel_name: str) -> list[TelegramPost]:
        posts = []
        # fixme - this is a hacky way to get all posts from a channel (up to 50k)
        for post_id in tqdm(range(1, 30)):
            post = self.fetch_post(post_id=post_id, channel_name=channel_name)
            posts.append(post)
        return posts

    def _request_html(self, post_url: str) -> BeautifulSoup:
        response = requests.get(url=post_url, headers=headers, timeout=10)
        response.raise_for_status()
        html_response = BeautifulSoup(response.text, "html.parser")
        return html_response
