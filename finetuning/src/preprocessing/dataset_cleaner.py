from datasets import load_dataset, Dataset
from src.config.model_config import (
    DOMAIN,
    PROCESSED_DATA_PATH,
)

import pandas as pd
import os


class DatasetCleaner:

    def load(self):

        dataset = load_dataset(
            "bitext/Bitext-customer-support-llm-chatbot-training-dataset"
        )

        return dataset["train"]

    def clean(self):

        data = self.load()

        print(f"Original samples : {len(data)}")

        # Remove invalid samples
        data = data.filter(
            lambda x:
            x["instruction"] is not None
            and x["response"] is not None
            and len(x["instruction"].strip()) > 3
            and len(x["response"].strip()) > 3
        )

        # Convert to DataFrame
        df = data.to_pandas()

        # Remove duplicate instruction-response pairs
        df = df.drop_duplicates(
            subset=[
                "instruction",
                "response",
            ]
        )

        print(f"After cleaning : {len(df)}")

        cleaned_dataset = Dataset.from_pandas(
            df,
            preserve_index=False,
        )

        output_path = os.path.join(
            PROCESSED_DATA_PATH,
            DOMAIN,
        )

        os.makedirs(
            output_path,
            exist_ok=True,
        )

        cleaned_dataset.save_to_disk(
            output_path
        )

        print(
            f"Saved cleaned dataset to {output_path}"
        )

        return cleaned_dataset


if __name__ == "__main__":

    cleaner = DatasetCleaner()

    cleaned = cleaner.clean()

    print(cleaned[0])