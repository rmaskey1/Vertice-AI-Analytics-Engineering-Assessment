from dataclasses import dataclass
import datetime
from typing import Optional

# Reordered dataclass attributes as non-default arguments cannot follow default arguments
#
# Original class format:
#
# @dataclass
# class MemberLevelScore():
#     client_account_id: str
#     member_id: str
#     level_score_type: str
#     score_date: Optional[datetime.date] = None
#     timestamp: Optional[datetime.datetime] = None
#     level_score: float
#     active_member: bool

@dataclass
class MemberLevelScore():
    client_account_id: str
    member_id: str
    level_score_type: str
    level_score: float
    active_member: bool
    score_date: Optional[datetime.date] = None
    timestamp: Optional[datetime.datetime] = None
