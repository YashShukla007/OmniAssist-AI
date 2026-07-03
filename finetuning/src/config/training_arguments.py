from trl import SFTConfig

from src.config.training_config import *


def get_training_arguments():

    return SFTConfig(

        output_dir=OUTPUT_DIR,

        num_train_epochs=NUM_EPOCHS,

        learning_rate=LEARNING_RATE,

        per_device_train_batch_size=TRAIN_BATCH_SIZE,

        gradient_accumulation_steps=GRADIENT_ACCUMULATION,

        warmup_ratio=WARMUP_RATIO,

        weight_decay=WEIGHT_DECAY,

        logging_steps=LOGGING_STEPS,

        save_steps=SAVE_STEPS,

        save_total_limit=2,

        bf16=True,

        logging_dir=LOGGING_DIR,

        report_to="none",

        remove_unused_columns=False,

        seed=42,

        lr_scheduler_type="cosine",

        optim="paged_adamw_8bit",

        dataloader_num_workers=2,

        dataset_text_field="text",

        max_length=MAX_SEQUENCE_LENGTH,

        packing=False,
    )