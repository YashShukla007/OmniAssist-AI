from src.comparison.compare_utils import (
    comparison_utils,
)

from src.comparison.compare_loader import (
    compare_loader,
)

from src.comparison.compare_inference import (
    compare_inference,
)

from src.comparison.compare_saver import (
    compare_saver,
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

        loaded_model, tokenizer = compare_loader.load_model(

            model,

        )

        outputs = compare_inference.generate(

            loaded_model,

            tokenizer,

        )

        compare_saver.save(

            model,

            outputs,

        )

        print(

            f"Generated {len(outputs)} responses."

        )

        del loaded_model

        del tokenizer

        print()


if __name__ == "__main__":

    main()