from datasets import load_dataset

from src.config.dpo_config import (
    DPO_DATASET_PATH,
)


class DPOFormatter:

    def load_dataset(self):

        dataset = load_dataset(

            "json",

            data_files=DPO_DATASET_PATH,

            split="train",

        )

        return dataset


dpo_formatter = DPOFormatter()