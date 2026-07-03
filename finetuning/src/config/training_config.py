# =====================================================
# Output Directories
# =====================================================

OUTPUT_DIR = "adapters/it_helpdesk"

LOGGING_DIR = "reports/logs"

# =====================================================
# Training Hyperparameters
# =====================================================

NUM_EPOCHS = 2

LEARNING_RATE = 2e-4

TRAIN_BATCH_SIZE = 2

GRADIENT_ACCUMULATION = 4

MAX_SEQUENCE_LENGTH = 1024

WARMUP_RATIO = 0.03

WEIGHT_DECAY = 0.01

LOGGING_STEPS = 10

SAVE_STEPS = 250

# =====================================================
# LoRA Configuration
# =====================================================

LORA_R = 16

LORA_ALPHA = 32

LORA_DROPOUT = 0.05

TARGET_MODULES = [
    "q_proj",
    "k_proj",
    "v_proj",
    "o_proj",
]