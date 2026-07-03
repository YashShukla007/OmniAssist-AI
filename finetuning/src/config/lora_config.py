from peft import LoraConfig, TaskType

from src.config.training_config import (
    LORA_R,
    LORA_ALPHA,
    LORA_DROPOUT,
    TARGET_MODULES,
)


def get_lora_config():

    return LoraConfig(

        r=LORA_R,

        lora_alpha=LORA_ALPHA,

        lora_dropout=LORA_DROPOUT,

        bias="none",

        task_type=TaskType.CAUSAL_LM,

        target_modules=TARGET_MODULES,

    )