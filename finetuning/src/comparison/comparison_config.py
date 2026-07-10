# =====================================================
# Models To Compare
# =====================================================

MODELS_TO_COMPARE = [

    # =================================================
    # Base Model
    # =================================================

    {

        "name": "Qwen Base",

        "description": "Original Qwen2.5-1.5B-Instruct base model without any fine-tuning.",

        "base_model": "Qwen/Qwen2.5-1.5B-Instruct",

        "model_type": "base",

        "adapter_source": None,

        "local_adapter_path": None,

        "hf_repo": None,

        "enabled": True,

    },

    # =================================================
    # Local SFT Adapter
    # =================================================

    {

        "name": "Qwen SFT (Local)",

        "description": "Supervised Fine-Tuned adapter stored locally for the Customer Support domain.",

        "base_model": "Qwen/Qwen2.5-1.5B-Instruct",

        "model_type": "sft",

        "adapter_source": "local",

        "local_adapter_path": "adapters/sft/it_helpdesk",

        "hf_repo": "YashShukla007/OmniAssist-SFT-IT-Helpdesk",

        "enabled": True,

    },

    # =================================================
    # Hugging Face SFT Adapter
    # =================================================

    {

        "name": "Qwen SFT (HF)",

        "description": "Supervised Fine-Tuned adapter loaded directly from Hugging Face.",

        "base_model": "Qwen/Qwen2.5-1.5B-Instruct",

        "model_type": "sft",

        "adapter_source": "huggingface",

        "local_adapter_path": "adapters/sft/it_helpdesk",

        "hf_repo": "YashShukla007/OmniAssist-SFT-IT-Helpdesk",

        "enabled": False,

    },

    # =================================================
    # Local DPO Adapter
    # =================================================

    {

        "name": "Qwen DPO (Local)",

        "description": "Direct Preference Optimization adapter stored locally for the Customer Support domain.",

        "base_model": "Qwen/Qwen2.5-1.5B-Instruct",

        "model_type": "dpo",

        "adapter_source": "local",

        "local_adapter_path": "adapters/dpo/it_helpdesk",

        "hf_repo": "YashShukla007/OmniAssist-DPO-IT-Helpdesk",

        "enabled": True,

    },

    # =================================================
    # Hugging Face DPO Adapter
    # =================================================

    {

        "name": "Qwen DPO (HF)",

        "description": "Direct Preference Optimization adapter loaded directly from Hugging Face.",

        "base_model": "Qwen/Qwen2.5-1.5B-Instruct",

        "model_type": "dpo",

        "adapter_source": "huggingface",

        "local_adapter_path": "adapters/dpo/it_helpdesk",

        "hf_repo": "YashShukla007/OmniAssist-DPO-IT-Helpdesk",

        "enabled": False,

    },

]