from .propensity_model import BasePropensityModel

class RulesBasedPropensityModel(BasePropensityModel):
    def __init__(self, eligibility_rules: dict):
        """
        :param eligibility_rules: Dictionary mapping product categories to eligibility functions
        """
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

    def _scoring_logic(self, member: dict, products: list, category: str, propensity_type: str) -> float:
        """
        Scoring logic for the rules-based model
        This function returns a constant value, but the scoring logic
        can be easily added/modified here by data scientists
        """
        return 1.0
