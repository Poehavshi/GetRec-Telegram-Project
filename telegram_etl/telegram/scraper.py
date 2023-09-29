import logging

import requests
from bs4 import BeautifulSoup

from telegram_etl.models.telegram import TelegramPost
from telegram_etl.telegram.html_parser import TelegramHTMLParser

logger = logging.getLogger(__name__)


class TelegramScraper:
    def __init__(self) -> None:
        self.headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/77.0.3865.90 Safari/537.36 TelegramBot (like TwitterBot)"
        }
        self.html_parser = TelegramHTMLParser()

    def run(self, channel_name: str, message_id: int) -> TelegramPost:
        post_url = f"https://t.me/{channel_name}/{message_id}?embed=1&mode=tme"
        try:
            html_response = self.request_html(post_url)
            post = self.html_parser.parse_one_post(html_response)
        except requests.exceptions.RequestException as error:
            logger.error(f"Error while requesting {post_url}: {error}")
            return TelegramPost(content="", author="", posted_at="", image_urls=[])
        else:
            return post

    def request_html(self, post_url: str) -> BeautifulSoup:
        response = requests.get(url=post_url, headers=self.headers, timeout=10)
        response.raise_for_status()
        html_response = BeautifulSoup(response.text, "html.parser")
        return html_response
