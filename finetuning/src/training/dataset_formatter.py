from datasets import Dataset


class DatasetFormatter:

    def format_chat_dataset(
        self,
        dataset: Dataset,
        tokenizer,
    ):

        def formatting_func(example):

            text = tokenizer.apply_chat_template(
                example["messages"],
                tokenize=False,
                add_generation_prompt=False,
            )

            return {
                "text": text
            }

        return dataset.map(formatting_func)


dataset_formatter = DatasetFormatter()