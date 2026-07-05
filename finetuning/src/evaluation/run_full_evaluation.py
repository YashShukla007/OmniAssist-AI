from src.evaluation.evaluate import (
    evaluate,
)

from src.evaluation.compare_models import (
    main as generate_report,
)


def main():

    print("=" * 60)
    print("Running Full Evaluation Pipeline")
    print("=" * 60)

    print("\nEvaluating Base Model...\n")

    evaluate("base")

    print("\nEvaluating SFT Model...\n")

    evaluate("sft")

    print("\nEvaluating DPO Model...\n")

    evaluate("dpo")

    print("\nGenerating Comparison Report...\n")

    generate_report()

    print("=" * 60)
    print("Evaluation Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":

    main()