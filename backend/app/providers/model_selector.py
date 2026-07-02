class ModelSelector:

    def __init__(self, models: str):

        self.models = [
            model.strip()
            for model in models.split(",")
            if model.strip()
        ]

    def get_models(self):

        return self.models