import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("dotReview_data.csv")

# Clean the column names
df.columns = ['name', 'energy_kcal', 'protein', 'carbohydrates', 'total_sugars', 'added_sugar', 
                'dietary_fiber', 'trans_fat', 'saturated_fat', 'total_fat', 'cholesterol_mg', 
                'sodium_mg', 'iron_mg', 'calcium_mg', 'ingredient_1', 'ingredient_2', 'ingredient_3', 
                'ingredient_4', 'ingredient_5', 'ingredient_6', 'ingredient_7', 'ingredient_8', 
                'ingredient_9']

# Drop unnecessary ingredient columns
df_cleaned = df.drop(columns=['ingredient_1', 'ingredient_2', 'ingredient_3', 'ingredient_4', 
                                  'ingredient_5', 'ingredient_6', 'ingredient_7', 'ingredient_8', 
                                  'ingredient_9'])

# Function to analyze product
def analyze_product(product_name):
    product = df_cleaned[df_cleaned['name'].str.contains(product_name, case=False, na=False)]
    
    if product.empty:
        st.error(f"Product '{product_name}' not found in the dataset.")
        return
    
    product = product.iloc[0]
    
    # Macronutrient composition pie chart
    macronutrient_values = [product['protein'], product['carbohydrates'], product['total_fat']]
    macronutrient_labels = ['Protein', 'Carbohydrates', 'Total Fat']
    fig_macronutrient = px.pie(values=macronutrient_values, names=macronutrient_labels, 
                               title=f'Macronutrient Composition of {product["name"]}')
    st.plotly_chart(fig_macronutrient)
    
    # Fat composition pie chart
    fat_values = [product['saturated_fat'], product['trans_fat'], 
                  product['total_fat'] - product['saturated_fat'] - product['trans_fat']]
    fat_labels = ['Saturated Fat', 'Trans Fat', 'Other Fat']
    fig_fat = px.pie(values=fat_values, names=fat_labels, title=f'Fat Composition of {product["name"]}')
    st.plotly_chart(fig_fat)
    
    # Distribution of added sugar vs. natural sugar pie chart (across all products)
    total_sugars = df_cleaned['total_sugars'].sum()
    added_sugar = df_cleaned['added_sugar'].sum()
    natural_sugar = total_sugars - added_sugar
    sugar_values = [added_sugar, natural_sugar]
    sugar_labels = ['Added Sugar', 'Natural Sugar']
    fig_sugar = px.pie(values=sugar_values, names=sugar_labels, title='Distribution of Added Sugar vs Natural Sugar')
    st.plotly_chart(fig_sugar)

    product = df_cleaned[df_cleaned['name'].str.contains(product_name, case=False, na=False)]
    
    if product.empty:
        print(f"Product '{product_name}' not found in the dataset.")
        return
    
    product = product.iloc[0]
    
    # Convert columns to numeric if they are not already
    numeric_columns = ['energy_kcal', 'protein', 'carbohydrates', 'total_sugars', 'added_sugar', 
                       'dietary_fiber', 'total_fat', 'saturated_fat', 'trans_fat', 
                       'cholesterol_mg', 'sodium_mg', 'iron_mg', 'calcium_mg']
    product[numeric_columns] = product[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
def product_nutritional_insights(product_name):
    product = df_cleaned[df_cleaned['name'].str.contains(product_name, case=False, na=False)]
    
    if product.empty:
        print(f"Product '{product_name}' not found in the dataset.")
        return
    
    product = product.iloc[0]
    insights = {}
    
    # Convert columns to numeric if they are not already
    numeric_columns = ['energy_kcal', 'protein', 'carbohydrates', 'total_sugars', 'added_sugar', 
                       'dietary_fiber', 'total_fat', 'saturated_fat', 'trans_fat', 
                       'cholesterol_mg', 'sodium_mg', 'iron_mg', 'calcium_mg']
    product[numeric_columns] = product[numeric_columns].apply(pd.to_numeric, errors='coerce')
    
    # Energy
    energy_percent = (product['energy_kcal'] / 2000) * 100
    insights['Energy'] = f"{product['energy_kcal']} kcal ({energy_percent:.2f}% of daily intake)"
    
    # Protein
    protein_percent = (product['protein'] / 56) * 100  # Using RDA for men
    insights['Protein'] = f"{product['protein']} g ({protein_percent:.2f}% of daily intake)"
    
    # Carbohydrates
    carbs_percent = (product['carbohydrates'] / 300) * 100  # Using midpoint of 225-325 g range
    insights['Carbohydrates'] = f"{product['carbohydrates']} g ({carbs_percent:.2f}% of daily intake)"
    
    # Total Sugars
    sugars_percent = (product['total_sugars'] / 50) * 100
    insights['Total Sugars'] = f"{product['total_sugars']} g ({sugars_percent:.2f}% of daily limit)"
    
    # Added Sugar
    added_sugar_percent = (product['added_sugar'] / 50) * 100
    insights['Added Sugar'] = f"{product['added_sugar']} g ({added_sugar_percent:.2f}% of daily limit)"
    
    # Dietary Fiber
    fiber_percent = (product['dietary_fiber'] / 38) * 100   
    insights['Dietary Fiber'] = f"{product['dietary_fiber']} g ({fiber_percent:.2f}% of daily intake)"
    
    # Total Fat
    fat_percent = (product['total_fat'] / 78) * 100  # Using upper limit of 20-35% range
    insights['Total Fat'] = f"{product['total_fat']} g ({fat_percent:.2f}% of daily intake)"
    
    # Saturated Fat
    sat_fat_percent = (product['saturated_fat'] / 20) * 100
    insights['Saturated Fat'] = f"{product['saturated_fat']} g ({sat_fat_percent:.2f}% of daily limit)"
    
    # Trans Fat
    trans_fat_percent = (product['trans_fat'] / 2) * 100
    insights['Trans Fat'] = f"{product['trans_fat']} g ({trans_fat_percent:.2f}% of daily limit)"
    
    # Cholesterol
    insights['Cholesterol'] = f"{product['cholesterol_mg']} mg"
    
    # Sodium
    sodium_percent = (product['sodium_mg'] / 2300) * 100
    insights['Sodium'] = f"{product['sodium_mg']} mg ({sodium_percent:.2f}% of daily limit)"
    
    # Iron
    iron_percent = (product['iron_mg'] / 18) * 100  # Using RDA for women
    insights['Iron'] = f"{product['iron_mg']} mg ({iron_percent:.2f}% of daily intake)"
    
    # Calcium
    calcium_percent = (product['calcium_mg'] / 1000) * 100
    insights['Calcium'] = f"{product['calcium_mg']} mg ({calcium_percent:.2f}% of daily intake)"
    
    return insights

# Streamlit app
st.title('Product Nutritional Analysis')

# Input for product name
product_name = st.text_input('Enter the product name:')

# Analyze button
if st.button('Analyze'):
    analyze_product(product_name)
    st.subheader('Nutritional Insights')
    insights = product_nutritional_insights(product_name)
    insights_table = [(nutrient, value) for nutrient, value in insights.items()]
    st.table(insights_table)

    import streamlit as st

    # Streamlit app
    st.title('Nutritional Information and Insights')

    st.markdown('''
    ### Energy (Calories)
    - **Daily Requirement**: The average adult requires about 2000-2500 kcal per day. This varies based on age, gender, activity level, and individual metabolic rate.
    - **Insight**: The products in the dataset seem to provide a significant amount of energy, often around 400-500 kcal per serving. This is about 20-25% of the daily requirement, so consumption should be moderate to avoid excessive calorie intake, especially if these are snacks or non-meal items.

    ### Protein
    - **Daily Requirement**: The Recommended Dietary Allowance (RDA) for protein is 46 grams per day for adult women and 56 grams per day for adult men.
    - **Insight**: Protein is essential for muscle repair and growth. The products in the dataset generally provide between 5-10 grams per serving, which is about 10-20% of the daily requirement. This makes them a moderate source of protein.

    ### Carbohydrates
    - **Daily Requirement**: Carbohydrates should make up about 45-65% of your total daily calories. For a 2000 kcal diet, this amounts to about 225-325 grams per day.
    - **Insight**: Many of these products are carbohydrate-dense, with around 70 grams per serving. This is about 20-30% of the daily requirement and should be balanced with other sources of carbohydrates like fruits, vegetables, and whole grains.

    ### Sugars (Total and Added)
    - **Daily Limit**: The WHO recommends that free sugars (added sugars and sugars naturally present in honey, syrups, and fruit juices) should be less than 10% of total energy intake. For a 2000 kcal diet, this is about 50 grams of sugar per day.
    - **Insight**: Many products have around 7 grams of total sugars, with varying amounts of added sugars. Keeping added sugar intake low is crucial to prevent health issues like obesity and tooth decay.

    ### Dietary Fiber
    - **Daily Requirement**: The RDA for dietary fiber is 25 grams per day for adult women and 38 grams per day for adult men.
    - **Insight**: Fiber is vital for digestive health. The products in the dataset generally have about 2 grams of fiber, which is around 5-10% of the daily requirement. It’s important to consume more fiber-rich foods like vegetables, fruits, legumes, and whole grains.

    ### Fats (Total, Saturated, and Trans Fat)
    - **Total Fat**: Should constitute 20-35% of your total daily calories. For a 2000 kcal diet, this is about 44-78 grams per day.
    - **Saturated Fat**: Should be less than 10% of total daily calories. For a 2000 kcal diet, this is about 20 grams per day.
    - **Trans Fat**: Should be kept as low as possible, ideally less than 1% of total daily calories (about 2 grams per day for a 2000 kcal diet).
    - **Insight**: Many products in the dataset have high total and saturated fat content. Keeping saturated and trans fats low is important to reduce the risk of heart disease.

    ### Cholesterol
    - **Daily Limit**: The American Heart Association recommends consuming less than 300 milligrams of cholesterol per day.
    - **Insight**: Some products may have cholesterol content, though it's often not listed. Monitoring intake from other sources like eggs, meat, and dairy is important.

    ### Sodium
    - **Daily Limit**: The American Heart Association recommends no more than 2300 milligrams of sodium per day, with an ideal limit of 1500 milligrams for most adults.
    - **Insight**: High sodium intake can lead to hypertension and other cardiovascular issues. It’s important to balance sodium intake from processed foods with fresh, whole foods.

    ### Iron and Calcium
    - **Iron**: The RDA for iron is 18 mg per day for adult women and 8 mg per day for adult men.
    - **Calcium**: The RDA for calcium is 1000 mg per day for most adults.
    - **Insight**: Adequate iron is important for preventing anemia, and calcium is crucial for bone health. The products in the dataset provide varying amounts of these minerals, so a balanced diet including other sources like leafy greens, nuts, seeds, and dairy is important.
    ''')