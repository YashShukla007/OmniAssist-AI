from peft import LoraConfig, TaskType

from src.config.training_config import (
    LORA_R,
    LORA_ALPHA,
    LORA_DROPOUT,
    TARGET_MODULES,
)


lora_config = LoraConfig(
    r=LORA_R,
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    target_modules=TARGET_MODULES,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)