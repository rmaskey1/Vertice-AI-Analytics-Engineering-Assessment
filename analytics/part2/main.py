import pandas as pd
from components.data_ingestion import load_data
from components.data_ingestion import get_member_products_by_category
from globals import PRODUCT_CATEGORIES, PRODUCT_CATEGORIES_LIST
from models.rules_based_model import RulesBasedPropensityModel
from models.ml_model import MLPropensityModel
from models.system import PropensityScoringSystem
from components.eligibility import eligibility_rules

"""
The main purpose of this file is to test the general flow of the system.
To see and test the modularity of the system, run "demo.py"
"""

def main():
    # Load the data
    members_df, member_products_df = load_data('../../data/members.csv', '../../data/member_product_accounts.csv')
    
    # Ensure member_id columns are strings
    members_df['member_id'] = members_df['member_id'].astype(str)
    member_products_df['member_id'] = member_products_df['member_id'].astype(str)

    test_members = members_df.head(1)
    
    # Initialize the Propensity Scoring System and register a rules-based model
    system = PropensityScoringSystem()
    # The rules-based model now contains its own scoring function internally.
    rules_model = RulesBasedPropensityModel(eligibility_rules)
    system.add_model('rules', rules_model)

    model_x = None  # Dummy pretrained machine learning model for MLPropensityModel
    ml_model = MLPropensityModel(model_x, eligibility_rules)
    system.add_model('ml', ml_model)
    
    results = []
    for _, member_row in test_members.iterrows():
        member = member_row.to_dict()
        member_id = member['member_id']
        member_result = {'member_id': member_id}
        
        # Get the member's product records, grouped by category
        products_by_category = get_member_products_by_category(member_id, member_products_df)
        
        # Loop over each defined product category
        for category in PRODUCT_CATEGORIES_LIST:
            # Retrieve the list of product records for this category
            products_list = products_by_category.get(category, [])
            
            # For each propensity type, call the model's score function
            for propensity_type in ['growth', 'churn']:
                score = system.score_member(member, products_list, category, propensity_type, 'rules') # model name can be switched out to either 'rules' or 'ml'
                key = f"{category}_{propensity_type}_score"
                member_result[key] = score
        
        results.append(member_result)
    
    # Convert the results list into a DataFrame and print.
    results_df = pd.DataFrame(results)
    pd.set_option('display.max_columns', None)
    print("Member-Level Propensity Scores:")
    print(results_df)
    results_df.to_csv('scores.csv', index=False)

if __name__ == '__main__':
    main()
