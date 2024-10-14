import streamlit as st

def render():
    st.header("Nutritional Guidelines")
    
    st.markdown('''
    ### Energy (Calories)
    - **Daily Requirement**: The average adult requires about 2000-2500 kcal per day. This varies based on age, gender, activity level, and individual metabolic rate.

    ### Protein
    - **Daily Requirement**: The Recommended Dietary Allowance (RDA) for protein is 46 grams per day for adult women and 56 grams per day for adult men.

    ### Carbohydrates
    - **Daily Requirement**: Carbohydrates should make up about 45-65% of your total daily calories. For a 2000 kcal diet, this amounts to about 225-325 grams per day.

    ### Sugars (Total and Added)
    - **Daily Limit**: The WHO recommends that free sugars (added sugars and sugars naturally present in honey, syrups, and fruit juices) should be less than 10% of total energy intake. For a 2000 kcal diet, this is about 50 grams of sugar per day.

    ### Dietary Fiber
    - **Daily Requirement**: The RDA for dietary fiber is 25 grams per day for adult women and 38 grams per day for adult men.
    - **Total Fat**: Should constitute 20-35% of your total daily calories. For a 2000 kcal diet, this is about 44-78 grams per day.
    - **Saturated Fat**: Should be less than 10% of total daily calories. For a 2000 kcal diet, this is about 20 grams per day.
    - **Trans Fat**: Should be kept as low as possible, ideally less than 1% of total daily calories (about 2 grams per day for a 2000 kcal diet).

    ### Cholesterol
    - **Daily Limit**: The American Heart Association recommends consuming less than 300 milligrams of cholesterol per day.

    ### Sodium
    - **Daily Limit**: The American Heart Association recommends no more than 2300 milligrams of sodium per day, with an ideal limit of 1500 milligrams for most adults.

    ### Iron and Calcium
    - **Iron**: The RDA for iron is 18 mg per day for adult women and 8 mg per day for adult men.
    - **Calcium**: The RDA for calcium is 1000 mg per day for most adults.
    ''')