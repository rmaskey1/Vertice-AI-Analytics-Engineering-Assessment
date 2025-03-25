import pandas as pd

from globals import PRODUCT_CATEGORIES, PRODUCT_CATEGORIES_LIST

def load_data(members_file: str, member_product_accounts_file: str):

    """
    Loads members and member product accounts data from CSV files and maps product category IDs to general categories
    """

    # Load members data
    members_df = pd.read_csv(members_file)
    
    # Load member product accounts data
    member_products_df = pd.read_csv(member_product_accounts_file)

    members_df['member_in_good_standing'] = members_df['member_in_good_standing'].astype(bool)
    
    # Map product_category_id to general product categories (checking, savings, personal_loans, etc.)
    def map_to_category(product_id: str) -> str:
        product_id = product_id.lower()
        for pattern, category in PRODUCT_CATEGORIES.items():
            if pattern in product_id:
                return category
        return 'other'

    # Apply mapping function 'product_category_id' column in member_products_df
    member_products_df['product_category'] = member_products_df['product_category_id'].apply(map_to_category)
    
    return members_df, member_products_df

def get_member_products_by_category(member_id: str, member_products: pd.DataFrame) -> dict:

    """
    Returns a dictionary with
    - Key: product category
    - Values: list of products of product category that belongs to member_id
    for every product category
    """

    # Filter the member products dataframe for member_id
    member_products['member_id'] = member_products['member_id'].astype(str)
    member_df = member_products[member_products['member_id'] == member_id]
    
    # Initialize products dictionary using PRODUCT_CATEGORIES_LIST from globals.py
    products = {category: [] for category in PRODUCT_CATEGORIES_LIST}
    
    # Iterate over each product row for this member
    for i, row in member_df.iterrows():
        product = row.to_dict()
        cat = product.get('product_category')
        if cat in products:
            products[cat].append(product)
    
    return products
