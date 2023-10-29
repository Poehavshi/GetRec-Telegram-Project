import os

from dagster import Definitions
from telegram_scrapping.assets import core_assets
from telegram_scrapping.jobs import (
    core_assets_schedule,
)
from telegram_scrapping.resources import RESOURCES_LOCAL

all_assets = [
    *core_assets,
]

resources_by_deployment_name = {
    "local": RESOURCES_LOCAL,
}

deployment_name = os.environ.get("DAGSTER_DEPLOYMENT", "local")

definitions = Definitions(
    assets=all_assets,
    resources=resources_by_deployment_name[deployment_name],
    schedules=[core_assets_schedule],
)
