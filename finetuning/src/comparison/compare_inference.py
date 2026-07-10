import json

from pathlib import Path

from src.inference.generator import (
    generator,
)


class CompareInference:

    def generate(

        self,

        model,

        tokenizer,

    ):

        prompts_path = Path(

            "evaluation/prompts.json"

        )

        with open(

            prompts_path,

            "r",

            encoding="utf-8",

        ) as f:

            prompts = json.load(f)

        outputs = []

        print("=" * 60)
        print("Generating Responses...")
        print("=" * 60)

        for sample in prompts:

            response = generator.generate(

                model,

                tokenizer,

                sample["prompt"],

            )

            outputs.append(

                {

                    "id": sample["id"],

                    "prompt": sample["prompt"],

                    "response": response,

                }

            )

            print(

                f"Completed Prompt {sample['id']}"

            )

        print("=" * 60)
        print("Inference Completed")
        print("=" * 60)

        return outputs


compare_inference = CompareInference()