import os

from telegram_scrapping.resources import TelegramRequestsClient
from telegram_scrapping.resources.telegram_resource import (
    download_images,
    download_video,
)

if __name__ == "__main__":
    telegram_client = TelegramRequestsClient()
    post = telegram_client.fetch_post(channel_name="complete_ai", post_id="254")
    image_urls = post.image_urls
    image_paths = download_images(image_urls)
    video_urls = post.video_urls
    os.makedirs("videos", exist_ok=True)
    video_paths = download_video(video_urls[0], f"videos/{0}.mp4")
