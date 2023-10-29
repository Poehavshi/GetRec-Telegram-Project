from telegram_scrapping.resources.parquet_io_manager import (
    LocalPartitionedParquetIOManager,
)
from telegram_scrapping.resources.telegram_resource import TelegramRequestsClient

RESOURCES_LOCAL = {
    "parquet_io_manager": LocalPartitionedParquetIOManager(),
    "telegram_client": TelegramRequestsClient(),
}
