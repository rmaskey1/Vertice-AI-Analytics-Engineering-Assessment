from abc import ABC, abstractmethod

class BasePropensityModel(ABC):
    @abstractmethod
    def score(self, member: dict, products: list, category: str, propensity_type: str) -> float:
        """
        Checks for user eligibility
        If user is eligible, invoke a scoring function that will return a float score value
        """
        pass
