import logging
from concurrent.futures import ProcessPoolExecutor
import pandas as pd

from telegram_etl.telegram.scraper import TelegramScraper

logger = logging.getLogger(__name__)


def parse_one_post() -> None:
    scraper = TelegramScraper()
    futures = []
    with ProcessPoolExecutor() as executor:
        for i in range(10):
            futures.append(executor.submit(scraper.run, channel_name="data_secrets", message_id=2402))
    # create csv file with all results
    for future in futures:
        post = future.result()
        df = pd.DataFrame(
            {
                "content": [post.content],
                "author": [post.author],
                "posted_at": [post.posted_at],
                "image_urls": [post.image_urls],
            }
        )
        df.to_csv("results.csv", mode="a", index=False, header=False)
    # todo add download images to some storage
    # todo add results to db or csv
    # todo add configuration for channels and message ids


if __name__ == "__main__":
    parse_one_post()
