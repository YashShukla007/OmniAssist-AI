from src.loaders.model_loader import (
    model_loader,
)


class CompareLoader:

    def load_model(

        self,

        model_info,

    ):

        print("=" * 60)
        print(f"Loading {model_info['name']}")
        print("=" * 60)

        if model_info["model_type"] == "base":

            model, tokenizer = model_loader.load(

                base_model=model_info["base_model"],

            )

        else:

            if model_info["adapter_source"] == "local":

                adapter_path = model_info["local_adapter_path"]

            else:

                adapter_path = model_info["hf_repo"]

            model, tokenizer = model_loader.load_for_inference(

                selected_model=model_info["model_type"],

                base_model=model_info["base_model"],

                adapter_path=adapter_path,

            )

        print("=" * 60)
        print(f"{model_info['name']} Loaded Successfully")
        print("=" * 60)

        return model, tokenizer


compare_loader = CompareLoader()