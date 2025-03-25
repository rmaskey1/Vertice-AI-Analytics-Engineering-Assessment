from datetime import datetime, timedelta
import pandas as pd

def checking_growth_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one checking account 
    with an account_open_date and no account_close_date
    """
    if checking_churn_indicator(products):  # Checking if member had account(s) but churned
        return False
    for prod in products:
        try:
            open_date = prod.get('account_open_date', '')
            close_date = prod.get('account_close_date', '')
        except (ValueError, TypeError):
            return False
        if open_date and (not close_date or pd.isna(close_date) or close_date == ''):
            return True
    return False

def checking_churn_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one checking account record, and 
    every checking account record meets the churn indicator:
      - If the account is closed (a valid account_close_date exists), it meets churn
      - Otherwise, account_transaction_count < 3 in the last 30 days
    """
    for prod in products:
        # Check if account is closed
        close_date = prod.get('account_close_date', '')
        if close_date and (not pd.isna(close_date) and close_date != ''):
            continue  # This record qualifies as churn because the account is closed
        try:
            transaction_count = int(prod.get('account_transaction_count', 0))
        except (ValueError, TypeError):
            return False
        if not (transaction_count < 3):
            return False
    return True

def savings_growth_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one savings account 
    with an account_open_date and no account_close_date
    """
    if savings_churn_indicator(products):   # Checking if member had account(s) but churned
        return False
    for prod in products:
        open_date = prod.get('account_open_date')
        close_date = prod.get('account_close_date')
        if open_date and (not close_date or pd.isna(close_date) or close_date == ''):
            return True
    return False

def savings_churn_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one savings account record, and
    every savings account record meets the churn indicator:
      - If the account is closed, it qualifies as churn
      - Otherwise, account_balance < $100 and the account has been open for at least 60 days
    """
    for prod in products:
        close_date = prod.get('account_close_date')
        if close_date and (not pd.isna(close_date) and close_date != ''):
            continue
        try:
            balance = float(prod.get('account_balance', 0))
        except (ValueError, TypeError):
            return False
        open_date_str = prod.get('account_open_date')
        if not open_date_str:
            return False
        try:
            open_date = datetime.strptime(open_date_str, '%Y-%m-%d')
        except Exception:
            return False
        if (datetime.now() - open_date).days < 60 or balance >= 100:
            return False
    return True

def personal_loans_growth_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one personal loan 
    with an account_open_date and no account_close_date
    """
    if personal_loans_churn_indicator(products):    # Checking if member had account(s) but churned
        return False
    for prod in products:
        open_date = prod.get('account_open_date')
        close_date = prod.get('account_close_date')
        if open_date and (not close_date or pd.isna(close_date) or close_date == ''):
            return True
    return False

def personal_loans_churn_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one personal loan record, and
    every personal loan record meets the churn indicator:
      - If the account is closed, it qualifies as churn
      - Otherwise, current balance < 80% of original balance
    """
    for prod in products:
        close_date = prod.get('account_close_date')
        if close_date and (not pd.isna(close_date) and close_date != ''):
            continue
        try:
            current_balance = float(prod.get('account_balance', 0))
            original_balance = float(prod.get('account_original_balance', 0))
        except (ValueError, TypeError):
            return False
        if original_balance <= 0 or current_balance >= 0.8 * original_balance:
            return False
    return True

def business_loans_growth_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one business loan 
    with an account_open_date and no account_close_date
    """
    if business_loans_churn_indicator(products):    # Checking if member had account(s) but churned
        return False
    for prod in products:
        open_date = prod.get('account_open_date')
        close_date = prod.get('account_close_date')
        if open_date and (not close_date or pd.isna(close_date) or close_date == ''):
            return True
    return False

def business_loans_churn_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one business loan record, and
    every business loan record meets the churn indicator:
      - If the account is closed, it qualifies as churn
      - Otherwise, monthly_payment missed or late
    Assumes that the product record has a boolean field 'monthly_payment_missed'
    """
    for prod in products:
        close_date = prod.get('account_close_date')
        if close_date and (not pd.isna(close_date) and close_date != ''):
            continue
        monthly_payment = prod.get('monthly_payment', False)
        if monthly_payment and not pd.isna(monthly_payment) and monthly_payment != '':
            return False
    return True

def certificates_growth_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one certificates/CD 
    with an account_open_date and no account_close_date
    """
    if certificates_churn_indicator(products):  # Checking if member had account(s) but churned
        return False
    for prod in products:
        open_date = prod.get('account_open_date')
        close_date = prod.get('account_close_date')
        if open_date and (not close_date or pd.isna(close_date) or close_date == ''):
            return True
    return False

def certificates_churn_indicator(products: list) -> bool:
    """
    Returns True if the member has at least one certificates/CD record, and
    every certificates/CD record meets the churn indicator:
      - If the account is closed, it qualifies as churn
      - Otherwise, today's date is within 30 days of term end (calculated as 
        account_open_date + product_term days) and there is no renewal activity
    Assumes 'product_term' is in days and 'renewal_activity' is a boolean flag
    """
    for prod in products:
        close_date = prod.get('account_close_date')
        if close_date and (not pd.isna(close_date) and close_date != ''):
            continue
        try:
            product_term = int(prod.get('product_term', 0))
        except Exception:
            return False
        open_date = prod.get('account_open_date')
        if not open_date:
            return False
        try:
            open_date = datetime.strptime(open_date, '%Y-%m-%d')
        except Exception:
            return False
        term_end = open_date + timedelta(days=product_term)
        days_to_term_end = (term_end - datetime.now()).days
        renewal_activity = prod.get('renewal_activity', False)
        if days_to_term_end > 30 or renewal_activity:
            return False
    return True
