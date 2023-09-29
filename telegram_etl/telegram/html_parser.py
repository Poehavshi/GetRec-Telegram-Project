import re

import html2text
from bs4 import BeautifulSoup

from telegram_etl.models.telegram import TelegramPost


class TelegramHTMLParser:
    def __init__(self) -> None:
        self.html_parser = html2text.HTML2Text()
        self.html_parser.body_width = 0  # Disable line wrapping
        self.html_parser.ignore_links = True  # Ignore hyperlinks
        self.html_parser.ignore_emphasis = True  # Ignore bold and italic formatting
        self.html_parser.ignore_images = True  # Ignore images
        self.html_parser.protect_links = True  # Protect hyperlinks from being stripped out
        self.html_parser.unicode_snob = True  # Use Unicode characters instead of ASCII
        self.html_parser.wrap_links = False  # Disable link wrapping
        self.html_parser.wrap_lists = False  # Disable list wrapping
        self.html_parser.decode_errors = "ignore"  # Ignore Unicode decoding errors

    def parse_one_post(self, html_of_post: BeautifulSoup) -> TelegramPost:
        content = self.parse_text_content(html_of_post)
        author = self.parse_author(html_of_post)
        date_time = self.parse_datetime(html_of_post)
        image_urls = self.parse_images(html_of_post)
        post = TelegramPost(content=content, author=author, posted_at=date_time, image_urls=image_urls)
        return post

    def parse_datetime(self, html_of_post: BeautifulSoup) -> str:
        date_time = self._html_to_text(
            str(html_of_post.find("span", {"class": "tgme_widget_message_meta"}).find("time", {"class": "datetime"}))
        )
        return date_time

    def parse_author(self, html_of_post: BeautifulSoup) -> str:
        author = self._html_to_text(
            str(
                html_of_post.find("div", {"class": "tgme_widget_message_author accent_color"})
                .find("a", {"class": "tgme_widget_message_owner_name"})
                .find("span", {"dir": "auto"})
            )
        )
        return author

    def parse_text_content(self, html_of_post: BeautifulSoup) -> str:
        content = self._html_to_text(
            str(
                html_of_post.find(
                    "div",
                    {
                        "class": "tgme_widget_message_text js-message_text",
                        "dir": "auto",
                    },
                )
            )
        )
        return content

    @staticmethod
    def parse_images(html_of_post: BeautifulSoup) -> list[str]:
        images_raw_urls = html_of_post.findAll("a", {"class": "tgme_widget_message_photo_wrap"})
        image_urls = []
        for div in images_raw_urls:
            style = div["style"]
            match = re.search(r"background-image:url\('(.*)'\)", style)
            if match:
                bg_image_url = match.group(1)
                image_urls.append(bg_image_url)
        return image_urls

    def _html_to_text(self, html_of_post: str) -> str:
        text = self.html_parser.handle(html_of_post)
        text = re.sub(r"\*+", "", text)  # Remove asterisks
        text = re.sub(r"^[ \t]*[\\`]", "", text, flags=re.MULTILINE)  # Remove leading \ or `
        return text
