from datasets import load_dataset


class ChatDatasetLoader:

    def load(
        self,
        dataset_path: str,
    ):

        dataset = load_dataset(
            "json",
            data_files=dataset_path,
        )

        return dataset["train"]


chat_dataset_loader = ChatDatasetLoader()