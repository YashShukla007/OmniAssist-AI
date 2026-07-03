import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
)

from src.config.model_config import (
    MODEL_NAME,
)


class ModelLoader:

    def load(self):

        bnb_config = BitsAndBytesConfig(

            load_in_4bit=True,

            bnb_4bit_quant_type="nf4",

            bnb_4bit_compute_dtype=torch.bfloat16,

            bnb_4bit_use_double_quant=True,

        )

        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
        )

        if tokenizer.pad_token is None:

            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(

            MODEL_NAME,

            quantization_config=bnb_config,

            device_map="auto",

            trust_remote_code=True,

        )

        return model, tokenizer


model_loader = ModelLoader()