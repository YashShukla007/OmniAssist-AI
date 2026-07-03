from datasets import load_dataset
from src.config.model_config import RAW_DATA_PATH

import os


class HFDatasetLoader:

    def download(self):

        print("Downloading dataset...")

        dataset = load_dataset(
            "bitext/Bitext-customer-support-llm-chatbot-training-dataset"
        )

        os.makedirs(
            RAW_DATA_PATH,
            exist_ok=True,
        )

        dataset.save_to_disk(
            os.path.join(
                RAW_DATA_PATH,
                "it_helpdesk",
            )
        )

        print(
            "\nDataset saved to:"
        )

        print(
            os.path.join(
                RAW_DATA_PATH,
                "it_helpdesk",
            )
        )

        return dataset


if __name__ == "__main__":

    loader = HFDatasetLoader()

    loader.download()