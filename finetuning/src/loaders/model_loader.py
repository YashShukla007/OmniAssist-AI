import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

from peft import (
    prepare_model_for_kbit_training,
)

from src.config.model_config import (
    MODEL_NAME,
)

from peft import PeftModel

from src.inference.inference_config import (
    MODEL_TYPE,
    SFT_ADAPTER_PATH,
    DPO_ADAPTER_PATH,
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
    
    
        def load_for_inference(self):

        model, tokenizer = self.load()

        if MODEL_TYPE == "base":

            print("=" * 60)
            print("Loaded Base Model")
            print("=" * 60)

            return model, tokenizer

        if MODEL_TYPE == "sft":

            print("=" * 60)
            print("Loading SFT Adapter...")
            print("=" * 60)

            model = PeftModel.from_pretrained(

                model,

                SFT_ADAPTER_PATH,

            )

            print("SFT Adapter Loaded Successfully")

            return model, tokenizer

        if MODEL_TYPE == "dpo":

            print("=" * 60)
            print("Loading DPO Adapter...")
            print("=" * 60)

            model = PeftModel.from_pretrained(

                model,

                DPO_ADAPTER_PATH,

            )

            print("DPO Adapter Loaded Successfully")

            return model, tokenizer

        raise ValueError(

            f"Unknown MODEL_TYPE: {MODEL_TYPE}"

        )


model_loader = ModelLoader()