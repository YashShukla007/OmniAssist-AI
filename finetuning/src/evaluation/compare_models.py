import json
from pathlib import Path


def load_json(file_path):

    with open(

        file_path,

        "r",

        encoding="utf-8",

    ) as f:

        return json.load(f)


def main():

    evaluation_dir = Path("evaluation")

    base_file = evaluation_dir / "base_outputs.json"

    sft_file = evaluation_dir / "sft_outputs.json"

    dpo_file = evaluation_dir / "dpo_outputs.json"

    base_outputs = load_json(base_file)

    sft_outputs = load_json(sft_file)

    dpo_outputs = load_json(dpo_file)

    report_path = (
        evaluation_dir
        / "comparison_report.md"
    )

    with open(

        report_path,

        "w",

        encoding="utf-8",

    ) as report:

        report.write("# OmniAssist Evaluation Report\n\n")

        report.write(
            "## Base vs SFT vs DPO\n\n"
        )

        for base, sft, dpo in zip(

            base_outputs,

            sft_outputs,

            dpo_outputs,

        ):

            report.write(
                f"## Prompt {base['id']}\n\n"
            )

            report.write(
                "### User Prompt\n"
            )

            report.write(
                f"{base['prompt']}\n\n"
            )

            report.write(
                "### Base Model\n"
            )

            report.write(
                base["response"]
            )

            report.write(
                "\n\n"
            )

            report.write(
                "### SFT Model\n"
            )

            report.write(
                sft["response"]
            )

            report.write(
                "\n\n"
            )

            report.write(
                "### DPO Model\n"
            )

            report.write(
                dpo["response"]
            )

            report.write(
                "\n\n"
            )

            report.write(
                "---\n\n"
            )

    print("=" * 60)
    print("Comparison Report Generated Successfully!")
    print(report_path)
    print("=" * 60)


if __name__ == "__main__":

    main()