from dataclasses import dataclass


@dataclass
class Level():
    client_account_id: str
    level_id: str
    level_name: str
    level_score_start: int
    level_score_end: int
