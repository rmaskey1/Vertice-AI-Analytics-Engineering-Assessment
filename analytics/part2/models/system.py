class PropensityScoringSystem:
    def __init__(self):
        """
        Creating a registry to store loaded models
        """
        self.models = {}  # Registry for propensity models

    def add_model(self, name: str, model):
        """
        Key: name of model
        Value: initialized model object

        For this project, the existing model types are RulesBasedPropensityModel() and MLPropensityModel()
        """
        self.models[name] = model

    def score_member(self, member: dict, products: list, category: str, propensity_type: str, model_name: str) -> float:
        """
        Checks to see if model exists in registry
        If it does, the "score" function for the corresponding model will be invoked
        """
        model = self.models.get(model_name)
        if not model:
            raise ValueError(f"Model '{model_name}' is not registered.")
        return model.score(member, products, category, propensity_type)
