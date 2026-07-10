import json

from pathlib import Path


class PromptLoader:

    def load(self):

        prompts_path = Path(

            "evaluation/prompts.json"

        )

        with open(

            prompts_path,

            "r",

            encoding="utf-8",

        ) as f:

            prompts = json.load(f)

        return prompts


prompt_loader = PromptLoader()