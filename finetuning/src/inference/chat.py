from src.loaders.model_loader import (
    model_loader,
)

from src.inference.generator import (
    generator,
)

from src.inference.inference_config import (
    MODEL_TYPE,
)


def main():

    print("=" * 60)
    print("OmniAssist Inference")
    print("=" * 60)

    print(f"Model Type : {MODEL_TYPE}")

    print("=" * 60)
    print("Loading Model...")
    print("=" * 60)

    model, tokenizer = model_loader.load_for_inference()

    model.eval()

    print("=" * 60)
    print("Model Ready!")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:

        prompt = input("\nYou : ")

        if prompt.lower() in ["exit", "quit"]:

            print("\nGoodbye!")
            break

        response = generator.generate(

            model,

            tokenizer,

            prompt,

        )

        print("\nAssistant :")

        print(response)


if __name__ == "__main__":

    main()