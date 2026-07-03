from datasets import load_from_disk
from src.config.model_config import (
    DOMAIN,
    PROCESSED_DATA_PATH,
    PREFERENCE_DATA_PATH,
)

import random
import json
import os


class PreferenceGenerator:

    def generate(self):

        input_path = os.path.join(
            PROCESSED_DATA_PATH,
            DOMAIN,
        )

        dataset = load_from_disk(input_path)

        output_dir = os.path.join(
            PREFERENCE_DATA_PATH,
            DOMAIN,
        )

        os.makedirs(
            output_dir,
            exist_ok=True,
        )

        output_file = os.path.join(
            output_dir,
            "preference_dataset.jsonl",
        )

        rows = list(dataset)

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            for idx, row in enumerate(rows):

                same_category = [

                    r for r in rows

                    if (
                        r["category"] == row["category"]
                        and r["response"] != row["response"]
                    )

                ]

                if len(same_category) == 0:
                    continue

                rejected = random.choice(
                    same_category
                )

                sample = {

                    "id": idx,

                    "prompt": row["instruction"],

                    "chosen": row["response"],

                    "rejected": rejected["response"],

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
            f"\nSaved preference dataset to:\n{output_file}"
        )


if __name__ == "__main__":

    generator = PreferenceGenerator()

    generator.generate()