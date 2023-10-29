import os

import requests
from dagster import Output, asset
from pandas import DataFrame
from telegram_scrapping.resources.telegram_resource import TelegramClient


@asset(io_manager_key="parquet_io_manager", key_prefix=["s3", "core"])
def posts(context, telegram_client: TelegramClient, channel_names) -> Output[DataFrame]:
    """Posts from the telegram channels."""

    context.log.info(f"Downloading posts from channels: {channel_names}")
    rows = []
    for channel in channel_names:
        rows.extend(telegram_client.fetch_posts_from_channel(channel))
        if len(rows) % 100 == 0:
            context.log.info(f"Downloaded {len(rows)} items!")

    non_none_rows = [row.dict() for row in rows if row is not None]
    result = DataFrame(non_none_rows)
    return Output(
        result,
        metadata={"Count": len(non_none_rows)},
    )


def download_images(image_urls: list[str]) -> list[str]:
    image_paths = []
    os.makedirs("images", exist_ok=True)
    for image_url in image_urls:
        image_path = f"images/{image_url.split('/')[-1][-20:]}"
        download_image(image_url, image_path)
        image_paths.append(image_path)
    return image_paths


def download_image(image_url: str, image_path: str) -> None:
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the content of the response (the image data)
        image_data = response.content
        # Write the image data to a file
        with open(image_path, "wb") as file:
            file.write(image_data)
        print("Image downloaded successfully!")
    else:
        print("Failed to download image.")


@asset()
def downloaded_images(posts: DataFrame) -> Output[DataFrame]:
    """Download images from the posts. Return the dataframe with the images metadata."""
    image_urls = posts["image_url"].dropna().unique().tolist()
    image_paths = download_images(image_urls)
    image_data = [
        {"image_url": image_url, "image_path": image_path}
        for image_url, image_path in zip(image_urls, image_paths)
    ]
    result = DataFrame(image_data)
    return Output(
        result,
        metadata={"Count": len(result)},
    )
