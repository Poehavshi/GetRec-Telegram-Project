import os

import pandas
from dagster import (
    ConfigurableIOManager,
    InputContext,
    OutputContext,
)
from dagster._seven import get_system_temp_directory


class PartitionedParquetIOManager(ConfigurableIOManager):
    """
    This IOManager will take in a pandas dataframe and store it in parquet at the
    specified path.

    Downstream ops can either load this dataframe into a spark session or simply retrieve a path
    to where the data is stored.
    """

    @property
    def _base_path(self):
        raise NotImplementedError()

    def handle_output(self, context: OutputContext, obj: pandas.DataFrame):
        path = self._get_path(context)
        if "://" not in self._base_path:
            os.makedirs(os.path.dirname(path), exist_ok=True)

        if isinstance(obj, pandas.DataFrame):
            row_count = len(obj)
            context.log.info(f"Row count: {row_count}")
            obj.to_parquet(path=path, index=False)
        else:
            raise TypeError(f"Outputs of type {type(obj)} not supported.")

        context.add_output_metadata({"row_count": row_count, "path": path})

    def load_input(self, context) -> str:
        path = self._get_path(context)
        return path

    def _get_path(self, context: InputContext | OutputContext):
        key = context.asset_key.path[-1]
        return os.path.join(self._base_path, f"{key}.pq")


class LocalPartitionedParquetIOManager(PartitionedParquetIOManager):
    base_path: str = get_system_temp_directory()

    @property
    def _base_path(self):
        return self.base_path


class S3PartitionedParquetIOManager(PartitionedParquetIOManager):
    s3_bucket: str

    @property
    def _base_path(self):
        return "s3://" + self.s3_bucket
