from src.preprocessing.dataset_cleaner import (
    DatasetCleaner,
)

from src.preprocessing.chat_generator import (
    ChatGenerator,
)

from src.preprocessing.instruction_generator import (
    InstructionGenerator,
)

from src.preprocessing.preference_generator import (
    PreferenceGenerator,
)


class DatasetExporter:

    def export(self):

        print("=" * 60)
        print("Running Complete Dataset Pipeline")
        print("=" * 60)

        cleaner = DatasetCleaner()
        cleaner.clean()

        print()

        chat = ChatGenerator()
        chat.generate()

        print()

        instruction = InstructionGenerator()
        instruction.generate()

        print()

        preference = PreferenceGenerator()
        preference.generate()

        print()
        print("=" * 60)
        print("Dataset Pipeline Completed Successfully")
        print("=" * 60)


if __name__ == "__main__":

    exporter = DatasetExporter()

    exporter.export()