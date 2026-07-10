import json

from pathlib import Path


class CompareSaver:

    def save(

        self,

        model_info,

        outputs,

    ):

        output_dir = Path("comparison/outputs")

        output_dir.mkdir(

            parents=True,

            exist_ok=True,

        )

        filename = (

            model_info["name"]

            .lower()

            .replace(" ", "_")

            .replace("(", "")

            .replace(")", "")

            + ".json"

        )

        save_path = output_dir / filename

        with open(

            save_path,

            "w",

            encoding="utf-8",

        ) as f:

            json.dump(

                outputs,

                f,

                indent=4,

                ensure_ascii=False,

            )

        print("=" * 60)
        print(f"Saved : {save_path}")
        print("=" * 60)

        return save_path


compare_saver = CompareSaver()