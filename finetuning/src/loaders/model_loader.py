import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

from peft import (
    PeftModel,
    prepare_model_for_kbit_training,
)

from src.config.model_config import (
    MODEL_NAME,
)

from src.inference.inference_config import (
    MODEL_TYPE,
    ADAPTER_SOURCE,
    SFT_ADAPTER_PATH,
    DPO_ADAPTER_PATH,
    SFT_HF_REPO,
    DPO_HF_REPO,
)

class ModelLoader:

    def load(self):

        # =====================================================
        # QLoRA Quantization Configuration
        # =====================================================

        bnb_config = BitsAndBytesConfig(

            load_in_4bit=True,

            bnb_4bit_quant_type="nf4",

            bnb_4bit_compute_dtype=torch.bfloat16,

            bnb_4bit_use_double_quant=True,

        )

        # =====================================================
        # Tokenizer
        # =====================================================

        tokenizer = AutoTokenizer.from_pretrained(

            MODEL_NAME,

            trust_remote_code=True,

        )

        if tokenizer.pad_token is None:

            tokenizer.pad_token = tokenizer.eos_token

        tokenizer.padding_side = "right"

        # =====================================================
        # Base Model
        # =====================================================

        model = AutoModelForCausalLM.from_pretrained(

            MODEL_NAME,

            quantization_config=bnb_config,

            torch_dtype="auto",

            device_map="auto",

            trust_remote_code=True,

        )

        # =====================================================
        # Model Configuration
        # =====================================================

        model.config.use_cache = False

        model.config.pretraining_tp = 1

        # =====================================================
        # Enable Gradient Checkpointing
        # =====================================================

        model.gradient_checkpointing_enable()

        # =====================================================
        # Prepare Model for QLoRA Training
        # =====================================================

        model = prepare_model_for_kbit_training(model)

        return model, tokenizer

    # =====================================================
    # Load Model for DPO Training
    # =====================================================

    def load_for_dpo(self):

        model, tokenizer = self.load()

        print("=" * 60)
        print("Loading SFT Adapter for DPO Training...")
        print("=" * 60)

        if ADAPTER_SOURCE == "local":
            adapter_path = SFT_ADAPTER_PATH
        else:
            adapter_path = SFT_HF_REPO

        model = PeftModel.from_pretrained(
            model,
            adapter_path,
            is_trainable=True,
        )

        print("=" * 60)
        print("SFT Adapter Loaded Successfully")
        print("=" * 60)

        return model, tokenizer

    # =====================================================
    # Load Model for Inference
    # =====================================================

    def load_for_inference(
        self,
        selected_model=None,
    ):

        model, tokenizer = self.load()

        selected_model = selected_model or MODEL_TYPE

        if selected_model == "base":

            print("=" * 60)
            print("Loaded Base Model")
            print("=" * 60)

            return model, tokenizer

        if selected_model == "sft":

            print("=" * 60)
            print("Loading SFT Adapter...")
            print("=" * 60)

            adapter_path = (
                SFT_ADAPTER_PATH
                if ADAPTER_SOURCE == "local"
                else SFT_HF_REPO
            )

            print(f"Source : {ADAPTER_SOURCE}")
            print(f"Adapter : {adapter_path}")

            model = PeftModel.from_pretrained(

                model,

                adapter_path,

            )

            print("SFT Adapter Loaded Successfully")

            return model, tokenizer

        if selected_model == "dpo":

            print("=" * 60)
            print("Loading DPO Adapter...")
            print("=" * 60)

            adapter_path = (
                DPO_ADAPTER_PATH
                if ADAPTER_SOURCE == "local"
                else DPO_HF_REPO
            )

            print(f"Source : {ADAPTER_SOURCE}")
            print(f"Adapter : {adapter_path}")

            model = PeftModel.from_pretrained(

                model,

                adapter_path,

            )

            print("DPO Adapter Loaded Successfully")

            return model, tokenizer

        raise ValueError(

            f"Unknown MODEL_TYPE: {selected_model}"

        )


model_loader = ModelLoader()