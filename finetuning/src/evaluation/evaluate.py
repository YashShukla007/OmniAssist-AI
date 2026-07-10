from src.evaluation.prompt_loader import (
    prompt_loader,
)

from src.loaders.model_loader import (
    model_loader,
)

from src.inference.generator import (
    generator,
)

from src.inference.inference_config import (
    MODEL_TYPE,
)


def evaluate(selected_model=None):

    print("=" * 60)
    print("Loading Model...")
    print("=" * 60)

    model, tokenizer = model_loader.load_for_inference(
    selected_model=selected_model,
)

    model.eval()

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

        print(f"Completed Prompt {sample['id']}")

    selected_model = selected_model or MODEL_TYPE

    save_path = (
        Path("evaluation")
        / f"{selected_model}_outputs.json"
    )

    with open(
        save_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(

            outputs,

            f,

            indent=4,

            ensure_ascii=False,

        )

    print("=" * 60)
    print(f"Saved outputs to {save_path}")
    print("=" * 60)


if __name__ == "__main__":

    evaluate()