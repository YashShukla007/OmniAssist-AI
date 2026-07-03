from pathlib import Path

from trl import SFTTrainer

from src.config.model_config import (
    CHAT_DATA_PATH,
    DOMAIN,
    SEED,
)

from src.config.lora_config import (
    get_lora_config,
)

from src.config.training_arguments import (
    get_training_arguments,
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

from src.utils.utils import (
    set_seed,
)


def main():

    # =====================================================
    # Set Seed
    # =====================================================

    set_seed(SEED)

    # =====================================================
    # Dataset Path
    # =====================================================

    dataset_path = str(
        Path(CHAT_DATA_PATH)
        / DOMAIN
        / "chat_dataset.jsonl"
    )

    # =====================================================
    # Load Dataset
    # =====================================================

    print("=" * 60)
    print("Loading chat dataset...")
    print("=" * 60)

    dataset = chat_dataset_loader.load(
        dataset_path
    )

    print(f"Samples : {len(dataset)}")

    # =====================================================
    # Load Model
    # =====================================================

    print("=" * 60)
    print("Loading model...")
    print("=" * 60)

    model, tokenizer = model_loader.load()

    print("Model Loaded Successfully")

    # =====================================================
    # Format Dataset
    # =====================================================

    print("=" * 60)
    print("Formatting dataset...")
    print("=" * 60)

    formatted_dataset = dataset_formatter.format_chat_dataset(
        dataset,
        tokenizer,
    )

    print(f"Formatted Samples : {len(formatted_dataset)}")

    print("=" * 60)
    print("Sample formatted conversation:")
    print("=" * 60)

    print(formatted_dataset[0]["text"][:1000])

    print("=" * 60)

    # =====================================================
    # Build Trainer
    # =====================================================

    print("=" * 60)
    print("Building SFT Trainer...")
    print("=" * 60)

    trainer = SFTTrainer(

        model=model,

        args=get_training_arguments(),

        train_dataset=formatted_dataset,

        processing_class=tokenizer,

        peft_config=get_lora_config(),

    )

    print("=" * 60)
    print("Trainer built successfully.")
    print("=" * 60)

    trainer.model.print_trainable_parameters()

    # =====================================================
    # Train
    # =====================================================

    print("=" * 60)
    print("Starting Training...")
    print("=" * 60)

    trainer.train()

    # =====================================================
    # Save Adapter
    # =====================================================

    print("=" * 60)
    print("Saving Adapter...")
    print("=" * 60)

    trainer.save_model()

    trainer.save_state()

    tokenizer.save_pretrained(
        trainer.args.output_dir
    )

    # =====================================================
    # Finished
    # =====================================================

    print("=" * 60)
    print("Training pipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":

    main()