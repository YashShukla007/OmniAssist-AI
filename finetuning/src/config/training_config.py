# =====================================================
# Output Directories
# =====================================================

OUTPUT_DIR = "adapters/sft/it_helpdesk"

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
# Training Dataset Configuration
# =====================================================

# Use a subset of the dataset during development.
# Set to None to train on the FULL dataset.
#
# Example:
# TRAIN_SUBSET_SIZE = 2000   -> Uses first 2000 samples
# TRAIN_SUBSET_SIZE = None   -> Uses entire dataset
#
# Recommended:
# - Development (Colab Free): 2000 or 5000 or any sample size depending upon whether your GPU can support or not, whether GPU limits may exhaust before total samples are processed...
# - Final Training (Better GPU): None

TRAIN_SUBSET_SIZE = 600

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