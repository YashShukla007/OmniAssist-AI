import torch

from src.inference.inference_config import (
    MAX_NEW_TOKENS,
    TEMPERATURE,
    TOP_P,
    DO_SAMPLE,
    REPETITION_PENALTY,
)


class ResponseGenerator:

    def generate(
        self,
        model,
        tokenizer,
        prompt: str,
    ):

        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = tokenizer(
            text,
            return_tensors="pt",
        ).to(model.device)

        with torch.no_grad():

            outputs = model.generate(

                **inputs,

                max_new_tokens=MAX_NEW_TOKENS,

                temperature=TEMPERATURE,

                top_p=TOP_P,

                do_sample=DO_SAMPLE,

                repetition_penalty=REPETITION_PENALTY,

                pad_token_id=tokenizer.pad_token_id,

                eos_token_id=tokenizer.eos_token_id,

            )

        generated = tokenizer.decode(

            outputs[0][inputs.input_ids.shape[-1]:],

            skip_special_tokens=True,

        )

        return generated.strip()


generator = ResponseGenerator()