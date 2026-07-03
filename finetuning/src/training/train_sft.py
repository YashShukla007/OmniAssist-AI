from pathlib import Path

from src.config.model_config import (
    CHAT_DATA_PATH,
    DOMAIN,
    SEED,
)

from src.utils.utils import (
    set_seed,
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

from peft import get_peft_model

from trl import SFTTrainer

from src.config.lora_config import (
    get_lora_config,
)

from src.config.training_arguments import (
    get_training_arguments,
)


def main():

    set_seed(SEED)

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

    print("=" * 60)
    print("Applying LoRA...")
    print("=" * 60)

    model = get_peft_model(
        model,
        get_lora_config(),
    )

    model.print_trainable_parameters()

    print("=" * 60)
    print("LoRA successfully attached.")
    print("=" * 60)

    print("=" * 60)
    print("Building Trainer...")
    print("=" * 60)

    trainer = SFTTrainer(

        model=model,

        args=get_training_arguments(),

        train_dataset=formatted_dataset,

        processing_class=tokenizer,

    )

    print("=" * 60)
    print("Starting Training...")
    print("=" * 60)

    trainer.train()

    print("=" * 60)
    print("Saving Adapter...")
    print("=" * 60)

    trainer.save_model()

    tokenizer.save_pretrained(
        trainer.args.output_dir
    )

    print("=" * 60)
    print("Training Completed Successfully!")
    print("=" * 60)

    print("=" * 60)
    print("Sample formatted conversation:")
    print("=" * 60)

    print(formatted_dataset[0]["text"][:1000])

    print("=" * 60)

    print("=" * 60)
    print("Everything loaded successfully.")
    print("=" * 60)


if __name__ == "__main__":

    main()