import pandas as pd
from components.data_ingestion import load_data, get_member_products_by_category
from globals import PRODUCT_CATEGORIES, PRODUCT_CATEGORIES_LIST
from components.eligibility import eligibility_rules
from models.rules_based_model import RulesBasedPropensityModel
from models.ml_model import MLPropensityModel
from models.system import PropensityScoringSystem

"""
Demo:

Allows user to self-input member_id, product categories to get scores for, propensity type, and model (if loaded to system)
"""

def propensity_score_retrieval(members_df, member_products_df, scoring_system):

    print("Available product categories: " + ", ".join(PRODUCT_CATEGORIES))
    print("Available models: 'rules', 'ml'")
    print("Enter member id, product categories, propensity type, and model name.")
    print("Type 'exit' to quit.\n")
    
    while True:
        # Prompt for member id
        member_id = input("Enter member id (or 'exit' to quit): ").strip()
        if member_id.lower() in ('exit', 'quit'):
            print("Exiting interactive mode.")
            break
        if not member_id:
            continue
        
        # Look up the member in members_df
        member_row = members_df[members_df['member_id'] == member_id]
        if member_row.empty:
            print(f"Member id '{member_id}' not found.")
            continue
        member = member_row.iloc[0].to_dict()
        
        # Prompt for product categories; if empty, use all
        print("Available product categories: " + ", ".join(PRODUCT_CATEGORIES_LIST))
        categories_input = input("Enter product categories (comma-separated) or press Enter for all: ").strip()
        if categories_input:
            categories = [c.strip() for c in categories_input.split(',')]
        else:
            categories = PRODUCT_CATEGORIES_LIST
        
        # Prompt for propensity type
        propensity_input = input("Enter propensity type (growth, churn, or both): ").strip().lower()
        if propensity_input in ['growth', 'churn']:
            propensity_types = [propensity_input]
        else:
            propensity_types = ['growth', 'churn']
        
        # Prompt for model choice
        model_name = input("Enter model name ('rules' or 'ml'): ").strip().lower()
        if model_name not in scoring_system.models.keys():
            print("Invalid model choice. Defaulting to 'rules'.")
            model_name = 'rules'
        
        # Retrieve this member's product records by category
        products_by_category = get_member_products_by_category(member_id, member_products_df)
        
        print(f"\nScores for member {member_id} using model '{model_name}':")
        for category in categories:
            prod_list = products_by_category.get(category, [])
            for ptype in propensity_types:
                score = scoring_system.score_member(member, prod_list, category, ptype, model_name)
                print(f"  {category:15} | {ptype:6} score: {score}")
        print("-" * 50)
        
def main():
    # Load data from CSV files
    members_df, member_products_df = load_data('../../data/members.csv', '../../data/member_product_accounts.csv')
    
    # Ensure member_id columns are strings
    members_df['member_id'] = members_df['member_id'].astype(str)
    member_products_df['member_id'] = member_products_df['member_id'].astype(str)
    
    # Initialize the scoring system and register a rules-based model
    scoring_system = PropensityScoringSystem()

    # Initialize rules-based propensity model + add it to the scoring system
    rules_model = RulesBasedPropensityModel(eligibility_rules)
    scoring_system.add_model('rules', rules_model)

    # Initialize ML propensity model + add it to the scoring system
    model_x = None  # Dummy pretrained machine learning model for MLPropensityModel
    ml_model = MLPropensityModel(model_x, eligibility_rules)
    scoring_system.add_model('ml', ml_model)
    
    # Start the loop
    propensity_score_retrieval(members_df, member_products_df, scoring_system)

if __name__ == '__main__':
    main()
