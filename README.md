# Analytics Engineering Assessment

Welcome to the Vertice analytics test project! We've structured this into two parts to get a good sense of both your hands-on analytics skills and your system design thinking.

## Part 1: Analytics Implementation

Let's start with some hands-on work to see how you handle analytics challenges. You'll be working with a synthetic dataset for a made-up "federal-cu" credit union (explained below).

### Context

The primary goal of this part is to output data for a metric we call "Levels Full" (Model - `models/LevelsFull.py`). This metric is used to understand the distribution and movement of members between levels.

Levels Explained: (File - `data/levels`, Model - `models/Level.py`)
To understand this task, you'll first need to understand Vertice levels. One core concept in the Vertice solution is the concept of "levels" of credit union membership. Think of this as a grade for your members (a member that has all their financial products with lots of money flowing through them all in the credit union might be level A while a member that just has a savings account would be level E).

Member Level Scores Explained: (File - `data/member_level_scores`, Model - `models/MemberLevelScore.py`)
Each member has a score that determines their level. This score is calculated based on the member's financial activity.

Level Explained: (File - `data/levels`, Model - `models/Level.py`)
Each client has a set of levels (that are defined outside of this project by clustering algorithms). Each level has a minimum and maximum score that a member must have to be in that level. Members are then assigned to the level that their score falls into.

Member Product Accounts Explained: (File - `data/member_product_accounts`, Model - `models/MemberProductAccount.py`)
Contains the financial accounts that a member has. This is where you can find products with their balances and other information.

History Files Explained:
Some items, like Member Level Scores, have history files. These files are used to track changes over time. For example, if a member's score changes, we want to know what it was at a specific point in time. In the case of Member Level Scores, the `data/member_level_scores_history` file has all the same fields as the `data/member_level_scores` file, but with an additional `timestamp` field. This field will be the same for all rows that are part of the same data-load.

### Requirements:

Create a working levels_full.py file that will output a completed LevelsFull metric. The LevelsFull model should explain what all
the fields are. Feel free to make assumptions, just note them down to explain later.

## Part 2: System Design Challenge

Now for the fun part! Design a framework for a propensity scoring system for a credit union. This system needs to predict how likely members are to either adopt new products (growth) or leave existing ones (churn).

### Requirements:

1. **Multi-Model Framework**

   - Support both rules-based models and ML classifiers
   - Make it easy for data scientists (who mainly know SQL + basic Python) to add new models
   - Models should be pluggable and configurable

2. **Product & Propensity Types**

   - Handle 5 product categories (checking, savings, personal loan, business loan, certificates)
   - Support both growth (likelihood to adopt a new product) and churn (likelihood to leave an existing product) propensity scoring

3. **Extra Considerations**

   a. **Eligibility Rules**

   - Members can't get growth scores for products they already have
   - Members can't get churn scores for products they don't have
   - Handle various eligibility rules (age requirements, regulatory constraints, etc.)
   - Make it easy to add/modify eligibility rules

   | Product Category   | Rules                                                                                                                                          |
   | ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
   | Checking           | • Member in good standing (`member_in_good_standing`)<br>• No closed checking accounts in last 90 days (`account_close_date`)                  |
   | Savings            | • Member in good standing (`member_in_good_standing`)<br>• Current total relationship balance < $100,000 (`member_total_relationship_balance`) |
   | Personal Loans     | • Member in good standing (`member_in_good_standing`)<br>• Estimated income > $24,000 (`member_estimated_income`)                              |
   | Business Loans     | • Member type is business (`member_current_type`)<br>• Member tenure > 2 years (`member_tenure`)                                               |
   | Certificates (CDs) | • Total relationship balance > $500 (`member_total_relationship_balance`)<br>• Member in good standing (`member_in_good_standing`)             |

b. **Product Status Logic**

- Different products have different adoption/churn definitions
- System should make it easy to define and modify these rules

  | Product Category   | Growth Logic                             | Churn Logic Indicator                                                                       |
  | ------------------ | ---------------------------------------- | ------------------------------------------------------------------------------------------- |
  | Checking Accounts  | New account opened (`account_open_date`) | `account_transaction_count` < 3 in last 30 days                                             |
  | Savings Accounts   | New account opened (`account_open_date`) | `account_balance` < $100 for 60+ days                                                       |
  | Personal Loans     | New loan opened (`account_open_date`)    | Current balance < 80% of original balance (`account_balance` vs `account_original_balance`) |
  | Business Loans     | New loan opened (`account_open_date`)    | `monthly_payment` missed or late                                                            |
  | Certificates (CDs) | New CD opened (`account_open_date`)      | Within 30 days of term end (`product_term`) with no renewal activity                        |

### Deliverables:

1. **System Design Document**

   - High-level architecture
   - Explanations of the reasoning behind the design

2. **Proof of Concept**
   - Implementation of core components
   - Example code for the whole system (doesn't have to run, just show us how you'd structure it)

## What We're Looking For

- Clean, maintainable code
- Smart handling of scale/performance
- Flexible, extensible architecture
- Clear documentation and reasoning
- Practical trade-offs and pragmatic choices

## Getting Started

1. Check out the `data/` directory for the sample dataset
2. Put your code in the `analytics/` directory
3. Create a repo with your code and share it with us
4. Have fun! And reach out if you have any questions

## Disclaimer

This is a new project so there may be some rough edges. If something doesn't seem right, let me (Luke) know!
