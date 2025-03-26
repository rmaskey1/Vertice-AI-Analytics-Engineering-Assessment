import os
import sys

# Get the absolute path of the parent directory of the current script and add parent directory to module search path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


import pandas as pd
from components.data_ingestion import get_member_products_by_category, load_data
from globals import PRODUCT_CATEGORIES_LIST
from components.eligibility import eligibility_rules

pd.set_option('display.max_columns', None)
members_df, member_products_df = load_data('../../../data/members.csv', '../../../data/member_product_accounts.csv')
test_members = members_df.head(2)   # Change this value to test for more members

for _, member_row in test_members.iterrows():
    member = member_row.to_dict()
    member_id = str(member['member_id'])
    print(f"\nEligibility for Member ID: {member_id}")
    
    # Retrieve this member's product records by category
    products_by_category = get_member_products_by_category(member_id, member_products_df)
    
    # Loop over each product category and test eligibility for both growth and churn
    for category in PRODUCT_CATEGORIES_LIST:
        # Get the list of product records for this category
        product_records = products_by_category.get(category, [])
        for propensity_type in ['growth', 'churn']:
            # Retrieve the eligibility function for this category
            eligibility_fn = eligibility_rules.get(category)
            # Call the eligibility function with the member and the list of product records
            eligible = eligibility_fn(member, product_records, propensity_type)
            print(f"Category: {category:15} | Propensity: {propensity_type:6} | Eligible: {eligible}")
