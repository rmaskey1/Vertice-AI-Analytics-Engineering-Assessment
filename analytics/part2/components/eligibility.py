from datetime import datetime
import pandas as pd
from .data_ingestion import get_member_products_by_category, load_data
from .product_status_logic import (
    checking_growth_indicator, checking_churn_indicator,
    savings_growth_indicator, savings_churn_indicator,
    personal_loans_growth_indicator, personal_loans_churn_indicator,
    business_loans_growth_indicator, business_loans_churn_indicator,
    certificates_growth_indicator, certificates_churn_indicator
)
from globals import PRODUCT_CATEGORIES, PRODUCT_CATEGORIES_LIST

def eligibility_check_checking(member: dict, products: list, propensity_type: str) -> bool:
    """
    Checking rules:
      - Member in good standing (member_in_good_standing)
      - No closed checking accounts in last 90 days (account_close_date)
      - For growth: member must not already have a checking account
      - For churn: member must have a checking account
    """
    if not member.get('member_in_good_standing', False):
        return False

    if propensity_type == 'growth':
        if checking_growth_indicator(products):
            return False
        
    elif propensity_type == 'churn':
        if not products or checking_churn_indicator(products):
            return False

    return True

def eligibility_check_savings(member: dict, products: list, propensity_type: str) -> bool:
    """
    Savings rules:
      - Member in good standing (member_in_good_standing)
      - Current total relationship balance < $100,000 (member_total_relationship_balance)
      - For growth: must not already have a savings account
      - For churn: must have a savings account
    """
    if not member.get('member_in_good_standing', False):
        return False

    try:
        balance = float(member.get('member_total_relationship_balance', 0))
        if balance >= 100000:
            return False
    except (ValueError, TypeError):
        return False

    if propensity_type == 'growth':
        if savings_growth_indicator(products):
            return False
        
    elif propensity_type == 'churn':
        if not products or savings_churn_indicator(products):
            return False

    return True

def eligibility_check_personal_loans(member: dict, products: list, propensity_type: str) -> bool:
    """
    Personal Loans rules:
      - Member in good standing (member_in_good_standing)
      - Estimated income > $24,000 (member_estimated_income)
      - For growth: must not already have a personal loan
      - For churn: must have a personal loan
    """
    if not member.get('member_in_good_standing', False):
        return False

    try:
        income = float(member.get('member_estimated_income', 0))
        if income <= 24000:
            return False
    except (ValueError, TypeError):
        return False

    if propensity_type == 'growth':
        if personal_loans_growth_indicator(products):
            return False
    elif propensity_type == 'churn':
        if not products or personal_loans_churn_indicator(products):
            return False

    return True

def eligibility_check_business_loans(member: dict, products: list, propensity_type: str) -> bool:
    """
    Business Loans rules:
      - Member type is business (member_current_type should equal 'business')
      - Member tenure > 2 years (member_tenure)
      - For growth: must not already have a business loan
      - For churn: must have a business loan
    """
    if member.get('member_current_type', '').lower() != 'business':
        return False

    try:
        tenure = float(member.get('member_tenure', 0))
        if tenure <= 2:
            return False
    except (ValueError, TypeError):
        return False

    if propensity_type == 'growth':
        if business_loans_growth_indicator(products):
            return False
    elif propensity_type == 'churn':
        if not products or business_loans_churn_indicator(products):
            return False

    return True

def eligibility_check_certificates(member: dict, products: list, propensity_type: str) -> bool:
    """
    Certificates (CDs) rules:
      - Total relationship balance > $500 (member_total_relationship_balance)
      - Member in good standing (member_in_good_standing)
      - For growth: must not already have a certificate/CD
      - For churn: must have a certificate/CD
    """
    try:
        balance = float(member.get('member_total_relationship_balance', 0))
        if balance <= 500:
            return False
    except (ValueError, TypeError):
        return False

    if not member.get('member_in_good_standing', False):
        return False

    if propensity_type == 'growth':
        if certificates_growth_indicator(products):
            return False
    elif propensity_type == 'churn':
        if not products or certificates_churn_indicator(products):
            return False

    return True

# Map product category keys to their corresponding eligibility functions
eligibility_rules = {
    'checking': eligibility_check_checking,
    'savings': eligibility_check_savings,
    'personal_loans': eligibility_check_personal_loans,
    'business_loans': eligibility_check_business_loans,
    'certificates': eligibility_check_certificates,
}
        

