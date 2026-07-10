import json

from pathlib import Path

from datetime import datetime

from src.comparison.compare_utils import (
    comparison_utils,
)

from src.comparison.compare_metrics import (
    compare_metrics,
)


class CompareReport:

    def generate(self):

        # =====================================================
        # Load Configuration
        # =====================================================

        models = comparison_utils.get_enabled_models()

        output_dir = Path("comparison/outputs")

        report_path = Path("comparison/comparison_report.md")

        model_outputs = {}

        # =====================================================
        # Load Output Files
        # =====================================================

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

                model_outputs[

                    model["name"]

                ] = json.load(f)

        total_prompts = len(

            next(

                iter(

                    model_outputs.values()

                )

            )

        )

        # =====================================================
        # Generate Markdown Report
        # =====================================================

        with open(

            report_path,

            "w",

            encoding="utf-8",

        ) as report:

            # =================================================
            # Title
            # =================================================

            report.write(

                "# OmniAssist AI Model Comparison Report\n\n"

            )

            report.write(

                f"**Generated On :** {datetime.now().strftime('%d %B %Y %H:%M:%S')}\n\n"

            )

            report.write(

                f"**Models Compared :** {len(models)}\n\n"

            )

            report.write(

                f"**Evaluation Prompts :** {total_prompts}\n\n"

            )

            report.write("---\n\n")

            # =================================================
            # Model Summary
            # =================================================

            report.write(

                "## Compared Models\n\n"

            )

            report.write(

                "| Model | Type | Source | Base Model |\n"

            )

            report.write(

                "|------|------|------|------|\n"

            )

            for model in models:

                report.write(

                    f"| {model['name']} | "

                    f"{model['model_type'].upper()} | "

                    f"{model['adapter_source'] or '-'} | "

                    f"{model['base_model']} |\n"

                )

            report.write("\n")

            # =================================================
            # Model Descriptions
            # =================================================

            report.write(

                "## Model Descriptions\n\n"

            )

            for model in models:

                report.write(

                    f"### {model['name']}\n\n"

                )

                report.write(

                    f"{model['description']}\n\n"

                )

            report.write("---\n\n")

            # =================================================
            # Prompt Comparisons
            # =================================================

            report.write(

                "# Prompt-wise Comparison\n\n"

            )

            for idx in range(total_prompts):

                prompt = model_outputs[

                    models[0]["name"]

                ][idx]["prompt"]

                report.write(

                    f"## Prompt {idx+1}\n\n"

                )

                report.write(

                    "### User Prompt\n\n"

                )

                report.write(

                    prompt

                )

                report.write("\n\n")

                for model in models:

                    response = model_outputs[

                        model["name"]

                    ][idx]["response"]

                    metrics = compare_metrics.calculate(
                        response
                    )

                    report.write(

                        f"### {model['name']}\n\n"

                    )

                    report.write(
                        f"**Words:** {metrics['words']}  \n"
                    )

                    report.write(
                        f"**Characters:** {metrics['characters']}  \n"
                    )

                    report.write(
                        f"**Sentences:** {metrics['sentences']}  \n"
                    )

                    report.write(
                        f"**Average Word Length:** {metrics['average_word_length']}  \n\n"
                    )

                    report.write(

                        response

                    )

                    report.write("\n\n")

                report.write(

                    "---\n\n"

                )

            # =================================================
            # Footer
            # =================================================

            report.write(

                "# End of Report\n"

            )

        print("=" * 60)
        print("Comparison Report Generated Successfully")
        print(report_path)
        print("=" * 60)


compare_report = CompareReport()