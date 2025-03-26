# Part 2: Propensity Scoring System

## Overview

Part 2 implements a complete propensity scoring framework to predict the **likelihood of a member to adopt (growth)** or **abandon (churn)** a specific financial product. The system supports multiple product categories and allows for different types of scoring models (rules-based and ML-based) to be easily registered, modified, and tested. It emphasizes modularity, configurability, and clarity while also enforcing eligibility rules and incorporating product-specific logic.

---

## System Structure

### 1. Product Categories

Defined in `globals.py`, the product categories include supported for scoring are:
- `checking`
- `savings`
- `personal_loans`
- `business_loans`
- `certificates`

These categories map detailed product IDs (e.g., "Premium Checking", "Basic CD") to consistent labels used throughout the system. Scoring support is not limited to just these 5 categories as the dictionary in `globals.py` can easily be modified to add or remove products supported for scoring.

---

### 2. Data Ingestion (`components/data_ingestion.py`)

**Responsibilities**
- Load, clean, and prepare `members.csv` and `member_product_accounts.csv` into Pandas Dataframes
- Normalize product names from `member_product_accounts.csv` into general categories via `map_to_category`
- `get_member_products_by_category`: maps each member to their product accounts per category
- Example output for `get_member_products_by_category`:
```python
{
    "checking": [
        {product_dictionary},
        {product_dictionary},
    ],
    "savings": [],
    "personal_loans": [],
    "business_loans": [
        {product_dictionary}
    ],
    "certificates": [
        {product_dictionary},
        {product_dictionary},
        {product_dictionary}
    ]
}
```

---

### 3. Product Status Logic (`components/product_status_logic.py`)

Defines how to **detect** product *adoption* (growth logic) or *abandonment* (churn logic) for each category:

| Product       | Growth Logic                              | Churn Logic                                             |
|---------------|--------------------------------------------|----------------------------------------------------------|
| Checking      | Open date exists + no close date           | Fewer than 3 transactions in last 30 days               |
| Savings       | Open date exists + no close date           | Balance < $100 for 60+ days                             |
| Personal Loan | Open date exists + no close date           | Current balance < 80% of original balance               |
| Business Loan | Open date exists + no close date           | Monthly payment missed/late                             |
| Certificates  | Open date exists + no close date           | Term ending within 30 days & no renewal activity        |

**Usage:**
This logic is NOT used for scoring but rather for **determining whether a member has adopted or churned**, which feeds into **eligibility** decisions.

---

### 4. Eligibility Rules (`components/eligibility.py`)

Eligibility is determined by a combination of:
- Member-level eligibility rules defined in the source code
- Propensity scoring type (growth or churn)
- Product status logic (whether the member has adopted or churned)

**Product Status Logic with Scoring**
- A member is not eligible for a **growth** score if they already have the product, meaning they satisfy the growth logic
- A member is not eligible for a **churn** score if they do **not** have the product, meaning they satisfy the churn logic
- **Assumptions**
    - It was assumed that having no account of a product does NOT count as a churn
    - If the churn logic is met by an account that has an open date but no close date, it is considered closed and that the user does not have the product anymore, making them eligible for growth scoring of that product type

---

### 5. Models

#### `BasePropensityModel`
- Base-level blueprint for all scoring models that can be used in the system
- Abstract method `score` sets a standard function that requires all propensity models to do a narrowed-down eligibility check on a member based on:
    1. Member data `member: dict`
    2. Member's product data `products: list`
    3. Product category `category: str`
    4. Propensity scoring type `propensity_type: str`
  If member passes these checks, a custom scoring logic function defined within the specific models is invoked

#### `RulesBasedPropensityModel`
- Initializes with a dictionary of product categories mapped to their respective eligibility function
- Implements eligibilty check
- If check is passed, invokes internal `_scoring_logic` function that applies rules-based scoring on the member
- Uses hardcoded scoring (returns `1.0` if eligible) for demonstration purposes

#### `MLPropensityModel`
- Initializes with a dictionary of product categories mapped to their respective eligibility function a pre-trained ML model
- Implements eligibilty check
- If check is passed, invokes internal `_scoring_logic` function that applies ML scoring on the member
- Currently uses a placeholder model for demonstration purposes

---

### 6. Propensity Scoring System (`models/system.py`)

- Registry of all scoring models for the scoring system
- Models are registered using `.add_model(model_name, model_instance)`
- Scoring is generalized using the `score_member` function, which checks to see if the model exists in the registry, then invokes the models own `score` function

---

### 7. CLI and Execution Scripts

#### `main.py`
- Testing the entire flow of the scoring system (data ingestion -> member-product mapping -> eligibility -> scoring)
- Tests first 20 members of `members.csv`
- Scores each member across all categories and both propensity types
- Uses "rules" model as default for the simplicity and function
- Outputs results to console and `scores.csv`

#### `demo.py`
- Allows interactive member scoring by ID
- Users can select product categories, model type (rules/ml), and propensity type for scoring
- Goes through flow and displays all requested scores

---

### 8. Additional Testing

#### `test_data_ingestion.py`
- Tests data ingestion functions `load_data` and `get_member_products_by_category`
- Outputs products by categories for a sample member_id

#### `test_eligibility.py`
- Tests eligibility functions for all product types
- Outputs eligibility status for both growth and churn score of all products types for 2 test members

---

## How to Run

### `main.py`

```bash
cd analytics\part2
python main.py
```

### `demo.py`

```bash
cd analytics\part2
python demo.py
```

### `test_data_ingestion.py`
```bash
cd analytics\part2\tests
python test_data_ingestion.py
```

### `test_eligibility.py`
```bash
cd analytics\part2\tests
python test_eligibility.py
```

## Future Improvements

- Integrate actual ML model training and predictions
- Add more model types
- Store scoring results in a database
- Create a simple web interface for score lookup
