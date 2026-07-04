from trl import (
    DPOTrainer,
)

from src.config.model_config import (
    SEED,
)

from src.config.dpo_training_arguments import (
    get_dpo_training_arguments,
)

from src.config.training_config import (
    TRAIN_SUBSET_SIZE,
)

from src.config.dpo_config import (
    DPO_OUTPUT_DIR,
)

from src.loaders.model_loader import (
    model_loader,
)

from src.training.dpo_formatter import (
    dpo_formatter,
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
    # Load Dataset
    # =====================================================

    print("=" * 60)
    print("Loading Preference Dataset...")
    print("=" * 60)

    dataset = dpo_formatter.load_dataset()

    # =====================================================
    # Use Dataset Subset (Development Only)
    # =====================================================

    if TRAIN_SUBSET_SIZE is not None:

        dataset = dataset.select(

            range(

                min(

                    TRAIN_SUBSET_SIZE,

                    len(dataset),

                )

            )

        )

    print(f"Samples : {len(dataset)}")
    print(dataset.column_names)

    print("=" * 60)
    print("Sample Preference:")
    print("=" * 60)

    print(dataset[0])

    print("=" * 60)

    # =====================================================
    # Load Model
    # =====================================================

    print("=" * 60)
    print("Loading Model...")
    print("=" * 60)

    model, tokenizer = model_loader.load()

    print("Model Loaded Successfully")

    training_args = get_dpo_training_arguments()

    # =====================================================
    # Build Trainer
    # =====================================================

    print("=" * 60)
    print("Building DPO Trainer...")
    print("=" * 60)

    trainer = DPOTrainer(

        model=model,

        ref_model=None,

        args=training_args,

        train_dataset=dataset,

        processing_class=tokenizer,

    )

    print("=" * 60)
    print("Trainer built successfully.")
    print("=" * 60)

    trainer.model.print_trainable_parameters()

    # =====================================================
    # Train
    # =====================================================

    print("=" * 60)
    print("Starting DPO Training...")
    print("=" * 60)

    trainer.train()

    # =====================================================
    # Save Adapter
    # =====================================================

    print("=" * 60)
    print("Saving Adapter...")
    print("=" * 60)

    trainer.save_model(
        DPO_OUTPUT_DIR
    )

    trainer.save_state()

    tokenizer.save_pretrained(
        DPO_OUTPUT_DIR
    )

    # =====================================================
    # Finished
    # =====================================================

    print("=" * 60)
    print("DPO Training Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":

    main()