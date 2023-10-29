from dagster import (
    AssetSelection,
    build_schedule_from_partitioned_job,
    define_asset_job,
)
from telegram_scrapping.assets import CORE
from telegram_scrapping.partitions import hourly_partitions

core_assets_schedule = build_schedule_from_partitioned_job(
    define_asset_job(
        "core_job",
        selection=AssetSelection.groups(CORE),
        partitions_def=hourly_partitions,
    ),
)
