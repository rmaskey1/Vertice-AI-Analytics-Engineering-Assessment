import os
import sys

# Get the absolute path of the parent directory of the current script and add parent directory to module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import pandas as pd
import random
import pprint
from components.data_ingestion import load_data, get_member_products_by_category
from globals import PRODUCT_CATEGORIES

members_df, member_products_df = load_data('../../data/members.csv', '../../data/member_product_accounts.csv')

sample_member_id = str(member_products_df['member_id'].iloc[0])
lookup = get_member_products_by_category(sample_member_id, member_products_df)

print("PRODUCT_CATEGORIES:", PRODUCT_CATEGORIES)
print(f"Products for member {sample_member_id}:")
pprint.pprint(lookup)