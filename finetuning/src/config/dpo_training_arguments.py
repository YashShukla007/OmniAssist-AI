from trl import (
    DPOConfig,
)

from src.config.dpo_config import (
    DPO_OUTPUT_DIR,
    DPO_NUM_EPOCHS,
    DPO_BATCH_SIZE,
    DPO_GRADIENT_ACCUMULATION_STEPS,
    DPO_LEARNING_RATE,
    DPO_BETA,
    DPO_MAX_PROMPT_LENGTH,
    DPO_MAX_LENGTH,
    DPO_LOGGING_STEPS,
    DPO_SAVE_STEPS,
)


def get_dpo_training_arguments():

    return DPOConfig(

        output_dir=DPO_OUTPUT_DIR,

        num_train_epochs=DPO_NUM_EPOCHS,

        per_device_train_batch_size=DPO_BATCH_SIZE,

        gradient_accumulation_steps=DPO_GRADIENT_ACCUMULATION_STEPS,

        learning_rate=DPO_LEARNING_RATE,

        beta=DPO_BETA,

        max_prompt_length=DPO_MAX_PROMPT_LENGTH,

        max_length=DPO_MAX_LENGTH,

        logging_steps=DPO_LOGGING_STEPS,

        save_steps=DPO_SAVE_STEPS,

        report_to="none",

        remove_unused_columns=False,

    )