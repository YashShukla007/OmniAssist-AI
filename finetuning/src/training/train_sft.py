from pathlib import Path

from src.config.model_config import (
    CHAT_DATA_PATH,
    DOMAIN,
)

from src.loaders.chat_dataset_loader import (
    chat_dataset_loader,
)

from src.loaders.model_loader import (
    model_loader,
)

from src.training.dataset_formatter import (
    dataset_formatter,
)


def main():

    dataset_path = str(
        Path(CHAT_DATA_PATH)
        / DOMAIN
        / "chat_dataset.jsonl"
    )

    print("=" * 60)
    print("Loading chat dataset...")
    print("=" * 60)

    dataset = chat_dataset_loader.load(
        dataset_path
    )

    print(f"Samples : {len(dataset)}")

    print("=" * 60)
    print("Loading model...")
    print("=" * 60)

    model, tokenizer = model_loader.load()

    print("Model Loaded Successfully")

    print("=" * 60)
    print("Formatting dataset...")
    print("=" * 60)

    formatted_dataset = (
        dataset_formatter.format_chat_dataset(
            dataset,
            tokenizer,
        )
    )

    print(formatted_dataset[0]["text"][:500])

    print("=" * 60)
    print("Everything loaded successfully.")
    print("=" * 60)


if __name__ == "__main__":

    main()