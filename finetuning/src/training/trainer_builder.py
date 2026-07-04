
#--------------------------- THIS FILE IS HAS OLDER IMPLEMENTATION CONFIGURATIONS USED EARLIER (NOT USEFUL NOW) -----------------------------

from trl import SFTTrainer
from transformers import TrainingArguments

from src.config.training_config import (
    OUTPUT_DIR,
    NUM_EPOCHS,
    LEARNING_RATE,
    TRAIN_BATCH_SIZE,
    GRADIENT_ACCUMULATION,
    LOGGING_STEPS,
    SAVE_STEPS,
)


class TrainerBuilder:

    def build(
        self,
        model,
        tokenizer,
        dataset,
        peft_config,
    ):

        args = TrainingArguments(

            output_dir=OUTPUT_DIR,

            learning_rate=LEARNING_RATE,

            per_device_train_batch_size=TRAIN_BATCH_SIZE,

            gradient_accumulation_steps=GRADIENT_ACCUMULATION,

            num_train_epochs=NUM_EPOCHS,

            logging_steps=LOGGING_STEPS,

            save_steps=SAVE_STEPS,

            report_to="none",

        )

        trainer = SFTTrainer(

            model=model,

            tokenizer=tokenizer,

            train_dataset=dataset,

            peft_config=peft_config,

            args=args,

            dataset_text_field="text",

        )

        return trainer


trainer_builder = TrainerBuilder()
