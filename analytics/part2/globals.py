"""
Global variables for product categories created for consistency.

In case another product category is added for scoring or removed from scoring, the change will only need to be made here
"""


PRODUCT_CATEGORIES = {
    'checking': 'checking',
    'savings': 'savings',
    'personal loan': 'personal_loans',
    'business': 'business_loans',
    'certificate': 'certificates',
    'cd': 'certificates'
}

PRODUCT_CATEGORIES_LIST = list({v for v in PRODUCT_CATEGORIES.values()})
