from src.comparison.compare_utils import (
    comparison_utils,
)


def main():

    print("=" * 60)
    print("Loading Comparison Configuration")
    print("=" * 60)

    models = comparison_utils.get_enabled_models()

    print()

    print(f"Enabled Models : {len(models)}")

    print()

    for model in models:

        comparison_utils.print_model_info(

            model,

        )


if __name__ == "__main__":

    main()