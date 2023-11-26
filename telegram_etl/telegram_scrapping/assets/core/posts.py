from dagster import Output, asset
from pandas import DataFrame
from telegram_scrapping.resources.telegram_resource import (
    TelegramClient,
    download_images,
)


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
