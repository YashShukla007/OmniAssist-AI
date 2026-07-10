from copy import deepcopy

from src.comparison.comparison_config import (
    MODELS_TO_COMPARE,
)


class ComparisonUtils:

    def get_enabled_models(self):

        return [

            deepcopy(model)

            for model in MODELS_TO_COMPARE

            if model["enabled"]

        ]

    def print_model_info(

        self,

        model,

    ):

        print("=" * 60)

        print(f"Name            : {model['name']}")

        print(f"Description     : {model['description']}")

        print(f"Base Model      : {model['base_model']}")

        print(f"Model Type      : {model['model_type']}")

        print(f"Adapter Source  : {model['adapter_source']}")

        print(f"Local Adapter   : {model['local_adapter_path']}")

        print(f"HF Repository   : {model['hf_repo']}")

        print("=" * 60)


comparison_utils = ComparisonUtils()