from src.evaluation.prompt_loader import (
    prompt_loader,
)

from src.inference.generator import (
    generator,
)


class CompareInference:

    def generate(

        self,

        model,

        tokenizer,

    ):

        prompts = prompt_loader.load()

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