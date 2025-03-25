from .propensity_model import BasePropensityModel

class MLPropensityModel(BasePropensityModel):
    def __init__(self, ml_model, eligibility_rules: dict):
        """
        :param ml_model: A pre-trained ML model
        :param eligibility_rules: Dictionary mapping product categories to eligibility functions
        """
        self.ml_model = ml_model
        self.eligibility_rules = eligibility_rules

    def score(self, member: dict, products: list, category: str, propensity_type: str) -> float:
        """
        Checks eligibility using the provided rules
        If eligible, invoke scoring logic
        """
        eligibility_fn = self.eligibility_rules.get(category)
        if eligibility_fn is None or not eligibility_fn(member, products, propensity_type):
            return None  # Not eligible.
        return self._scoring_logic(member, products, category, propensity_type)

    def _scoring_logic(self, member: dict, products: list, category: str, propensity_type: str) -> list:
        """
        Scoring logic for ML model can include using sklearn's predict or predict_proba
        on a set of extracted data to make a probability prediction
        
        Ex:
        
        features = extract_features(...)
        prob = self.ml_model.predict_proba(features)

        return prob

        """
        return 1.0
        
