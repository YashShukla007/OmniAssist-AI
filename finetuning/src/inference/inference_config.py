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

MODEL_TYPE = "dpo"
# base | sft | dpo


# =====================================================
# Adapter Source
# =====================================================

ADAPTER_SOURCE = "local"
# local | huggingface


# =====================================================
# Local Adapter Paths
# =====================================================

SFT_ADAPTER_PATH = "adapters/sft/it_helpdesk"

DPO_ADAPTER_PATH = "adapters/dpo/it_helpdesk"


# =====================================================
# Hugging Face Repositories
# =====================================================

SFT_HF_REPO = "YashShukla007/OmniAssist-SFT-IT-Helpdesk"

DPO_HF_REPO = "YashShukla007/OmniAssist-DPO-IT-Helpdesk"