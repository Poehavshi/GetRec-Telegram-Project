import pandas as pd
from dagster import Output, asset
from pandas import DataFrame


@asset()
def channels_csv_from_file() -> DataFrame:
    """Channels metadata parsed from telegram and stored as csv file"""
    # todo need to be specified in configuration
    return pd.read_csv(
        "/Users/arkadiysotnikov/PycharmProjects/GetRec-Telegram-Project/telegram_etl/data/raw/entity10k.csv"
    )


@asset()
def channel_names(channels_csv_from_file: DataFrame) -> Output[list]:
    """Channels names from the csv file"""
    return Output(
        list(channels_csv_from_file["username"]),
        metadata={"count": len(channels_csv_from_file)},
    )
