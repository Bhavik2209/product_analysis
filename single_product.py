import streamlit as st
import plotly.express as px
from utils import generate_nutritional_insights

def render(df):
    st.header("Single Product Analysis")
    
    product_name = st.text_input('Enter the product name:')

    if st.button('Analyze'):
        product = df[df['name'].str.contains(product_name, case=False, na=False)]
        
        if product.empty:
            st.error(f"Product '{product_name}' not found in the dataset.")
        else:
            product = product.iloc[0]
            st.subheader(f"Analysis for {product['name']}")
            
            st.write("Nutritional Information:")
            st.table(product.to_frame().T)
            
            daily_value_percentages = calculate_daily_value_percentage(product)
            st.subheader("Daily Value Percentages")
            for nutrient, percentage in daily_value_percentages.items():
                st.write(f"{nutrient}: {percentage}% of Daily Value")

            nutrient_ratios = calculate_nutrient_ratios(product)
            st.subheader("Nutrient Ratios")
            for ratio, value in nutrient_ratios.items():
                st.write(f"{ratio}: {value}")

            with st.spinner("Generating insights..."):
                insights = generate_nutritional_insights(product)
            st.write("AI-Generated Insights:")
            st.markdown(insights)
            
            fig_macro, fig_fat, fig_sugar = create_visualizations(product)
            st.plotly_chart(fig_macro)
            st.plotly_chart(fig_fat)
            st.plotly_chart(fig_sugar)

def calculate_daily_value_percentage(product):
    daily_values = {
        'energy_kcal': 2000,
        'protein': 50,
        'carbohydrates': 275,
        'dietary_fiber': 28,
        'total_fat': 78,
        'saturated_fat': 20,
        'cholesterol_mg': 300,
        'sodium_mg': 2300,
        'iron_mg': 18,
        'calcium_mg': 1000
    }
    
    return {nutrient: round((int(product[nutrient])/value) * 100, 2) 
            for nutrient, value in daily_values.items() if nutrient in product}

def calculate_nutrient_ratios(product):
    ratios = {
        'Protein to Carb Ratio': product['protein'] / product['carbohydrates'] if product['carbohydrates'] != 0 else 0,
        'Saturated to Unsaturated Fat Ratio': product['saturated_fat'] / (product['total_fat'] - product['saturated_fat']) if (product['total_fat'] - product['saturated_fat']) != 0 else 0,
        'Added to Total Sugar Ratio': product['added_sugar'] / product['total_sugars'] if product['total_sugars'] != 0 else 0
    }
    return {k: round(v, 2) for k, v in ratios.items()}

def create_visualizations(product):
    fig_macronutrient = px.pie(values=[product['protein'], product['carbohydrates'], product['total_fat']], 
                               names=['Protein', 'Carbohydrates', 'Total Fat'], 
                               title=f'Macronutrient Composition of {product["name"]}')
    
    fig_fat = px.pie(values=[product['saturated_fat'], product['trans_fat'], 
                             product['total_fat'] - product['saturated_fat'] - product['trans_fat']], 
                     names=['Saturated Fat', 'Trans Fat', 'Other Fat'], 
                     title=f'Fat Composition of {product["name"]}')
    
    fig_sugar = px.pie(values=[product['added_sugar'], product['total_sugars'] - product['added_sugar']], 
                       names=['Added Sugar', 'Natural Sugar'], 
                       title=f'Sugar Composition of {product["name"]}')
    
    return fig_macronutrient, fig_fat, fig_sugar