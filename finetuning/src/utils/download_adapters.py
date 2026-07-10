from pathlib import Path

from huggingface_hub import snapshot_download

from src.comparison.comparison_config import (
    MODELS_TO_COMPARE,
)


def download_adapter(model):

    if not model["enabled"]:

        return

    if model["adapter_source"] != "local":

        return

    adapter_path = model["adapter_path"]

    if adapter_path is None:

        return

    if Path(adapter_path).exists():

        print("=" * 60)
        print(f"{model['name']} already exists.")
        print("=" * 60)
        return

    repo_id = model.get("hf_repo")

    if repo_id is None:

        print("=" * 60)
        print(f"No HF repository specified for {model['name']}")
        print("=" * 60)
        return

    print("=" * 60)
    print(f"Downloading {model['name']}")
    print("=" * 60)

    snapshot_download(

        repo_id=repo_id,

        local_dir=adapter_path,

    )

    print("=" * 60)
    print(f"{model['name']} Downloaded Successfully")
    print("=" * 60)


def main():

    for model in MODELS_TO_COMPARE:

        download_adapter(model)


if __name__ == "__main__":

    main()