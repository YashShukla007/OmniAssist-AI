# =====================================================
# Inference Configuration
# =====================================================

# Generation Parameters

MAX_NEW_TOKENS = 256

TEMPERATURE = 0.7

TOP_P = 0.9

DO_SAMPLE = True

REPETITION_PENALTY = 1.1

# =====================================================
# Model Selection
# =====================================================

# "base"
# "sft"
# "dpo"

MODEL_TYPE = "sft"

# =====================================================
# Adapter Paths
# =====================================================

SFT_ADAPTER_PATH = "adapters/sft/it_helpdesk"

DPO_ADAPTER_PATH = "adapters/dpo/it_helpdesk"