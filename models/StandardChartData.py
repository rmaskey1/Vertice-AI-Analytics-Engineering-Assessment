from dataclasses import dataclass


@dataclass
class StandardDataPoint():
    key: str
    value: float

@dataclass
class StandardChartData():
    points: list[StandardDataPoint]
