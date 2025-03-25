from dataclasses import dataclass
from enum import Enum

@dataclass
class Timeline(Enum):
    OneMonth = "1m"
    ThreeMonths = "3m"
    SixMonths = "6m"
    TwelveMonths = "12m"
    YearToDate = "ytd"
