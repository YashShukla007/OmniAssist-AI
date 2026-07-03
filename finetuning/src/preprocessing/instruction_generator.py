from datasets import load_from_disk
from src.config.model_config import (
    DOMAIN,
    PROCESSED_DATA_PATH,
    INSTRUCTION_DATA_PATH,
)

import json
import os


class InstructionGenerator:

    def generate(self):

        input_path = os.path.join(
            PROCESSED_DATA_PATH,
            DOMAIN,
        )

        dataset = load_from_disk(input_path)

        output_dir = os.path.join(
            INSTRUCTION_DATA_PATH,
            DOMAIN,
        )

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

        output_file = os.path.join(
            output_dir,
            "instruction_dataset.jsonl",
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            for idx, row in enumerate(dataset):

                sample = {

                    "id": idx,

                    "instruction": row["instruction"],

                    "input": "",

                    "output": row["response"],

                    "metadata": {

                        "category": row["category"],

                        "intent": row["intent"],

                        "flags": row["flags"],

                    },

                }

                f.write(
                    json.dumps(
                        sample,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

        print(
            f"\nSaved instruction dataset to:\n{output_file}"
        )


if __name__ == "__main__":

    generator = InstructionGenerator()

    generator.generate()