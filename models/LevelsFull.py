
from dataclasses import dataclass
from models.Timeline import Timeline                         # Changed from "from src.model.Timeline" to "from Timeline"
from models.StandardChartData import StandardChartData       # Changed from "from src.model.StandardChartData" to "from StandardChartData"


@dataclass
class Movement():
    timeline: Timeline
    growth: int # The number of members that have moved up into this level in the timeline
    churn: int # The number of members that have moved down into this level in the timeline

@dataclass
class LevelData():
    level: str # The name of the level
    member_count: int # The number of members in this level
    score_start: float # The minimum score for this level
    score_end: float # The maximum score for this level
    avg_product_count: float # The average number of products per member in this level
    member_count_history: StandardChartData # A chart of the member count over time
    movement: list[Movement] # The movement of members in this level for each timeline

@dataclass
class LevelsFull():
    levels: list[LevelData]
