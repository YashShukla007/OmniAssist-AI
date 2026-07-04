# =====================================================
# DPO Training Configuration
# =====================================================

DPO_DATASET_PATH = "data/preference/it_helpdesk/preference_dataset.jsonl"

DPO_OUTPUT_DIR = "adapters/dpo/it_helpdesk"

DPO_NUM_EPOCHS = 2

DPO_BATCH_SIZE = 2

DPO_GRADIENT_ACCUMULATION_STEPS = 4

DPO_LEARNING_RATE = 5e-5

DPO_BETA = 0.1

DPO_MAX_PROMPT_LENGTH = 512

DPO_MAX_LENGTH = 1024

DPO_LOGGING_STEPS = 10

DPO_SAVE_STEPS = 150