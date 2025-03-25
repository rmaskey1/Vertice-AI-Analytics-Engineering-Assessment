from dataclasses import dataclass
import datetime
from typing import Optional

@dataclass
class MemberProductAccount:
    client_account_id: str
    account_id: str
    member_product_account_id: str
    member_id: str
    product_id: str
    product_category_id: str
    account_open_date: datetime.datetime
    account_balance: float
    account_transaction_count: int
    account_original_balance: float
    account_close_date: Optional[datetime.datetime] = None
    timestamp: Optional[datetime.datetime] = None
    product_rate: Optional[float] = None
    product_term: Optional[int] = None
    monthly_payment: Optional[float] = None
    credit_limit: Optional[float] = None
    collateral_description: Optional[str] = None
    collateral_attrib_1: Optional[str] = None
    collateral_attrib_2: Optional[str] = None
    collateral_attrib_3: Optional[str] = None
    collateral_attrib_4: Optional[str] = None
    count: Optional[int] = None