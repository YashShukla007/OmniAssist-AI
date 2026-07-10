import json

from pathlib import Path

from src.comparison.compare_utils import (
    comparison_utils,
)


class CompareReport:

    def generate(self):

        models = comparison_utils.get_enabled_models()

        output_dir = Path("comparison/outputs")

        report_path = Path("comparison/comparison_report.md")

        model_outputs = {}

        # ==========================================
        # Load all output files
        # ==========================================

        for model in models:

            filename = (

                model["name"]

                .lower()

                .replace(" ", "_")

                .replace("(", "")

                .replace(")", "")

                + ".json"

            )

            with open(

                output_dir / filename,

                "r",

                encoding="utf-8",

            ) as f:

                model_outputs[model["name"]] = json.load(f)

        # ==========================================
        # Generate Markdown Report
        # ==========================================

        with open(

            report_path,

            "w",

            encoding="utf-8",

        ) as report:

            report.write("# OmniAssist Model Comparison\n\n")

            report.write(f"Compared Models: {len(models)}\n\n")

            report.write("---\n\n")

            total_prompts = len(

                next(

                    iter(

                        model_outputs.values()

                    )

                )

            )

            for idx in range(total_prompts):

                report.write(

                    f"## Prompt {idx+1}\n\n"

                )

                report.write(

                    "**User Prompt**\n\n"

                )

                report.write(

                    model_outputs[

                        models[0]["name"]

                    ][idx]["prompt"]

                )

                report.write("\n\n")

                for model in models:

                    report.write(

                        f"### {model['name']}\n\n"

                    )

                    report.write(

                        model_outputs[

                            model["name"]

                        ][idx]["response"]

                    )

                    report.write("\n\n")

                report.write("---\n\n")

        print("=" * 60)
        print("Comparison Report Generated Successfully")
        print(report_path)
        print("=" * 60)


compare_report = CompareReport()