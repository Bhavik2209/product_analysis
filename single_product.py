import streamlit as st
import plotly.express as px
from utils import generate_nutritional_insights
import pandas as pd

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
            
            try:
                daily_value_percentages = calculate_daily_value_percentage(product)
                st.subheader("Daily Value Percentages")
                for nutrient, percentage in daily_value_percentages.items():
                    st.write(f"{nutrient}: {percentage}% of Daily Value")
            except Exception as e:
                st.error(f"Error calculating daily values: {str(e)}")

            try:
                nutrient_ratios = calculate_nutrient_ratios(product)
                st.subheader("Nutrient Ratios")
                for ratio, value in nutrient_ratios.items():
                    st.write(f"{ratio}: {value}")
            except Exception as e:
                st.error(f"Error calculating nutrient ratios: {str(e)}")

            try:
                with st.spinner("Generating insights..."):
                    insights = generate_nutritional_insights(product)
                st.write("AI-Generated Insights:")
                st.markdown(insights)
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")
            
            try:
                fig_macro, fig_fat, fig_sugar = create_visualizations(product)
                st.plotly_chart(fig_macro)
                st.plotly_chart(fig_fat)
                st.plotly_chart(fig_sugar)
            except Exception as e:
                st.error(f"Error creating visualizations: {str(e)}")

def safe_float_conversion(value):
    """Safely convert a value to float, handling various input types."""
    try:
        if pd.isna(value) or value == '' or value is None:
            return 0.0
        return float(str(value).strip())
    except (ValueError, TypeError):
        return 0.0

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
    
    percentages = {}
    for nutrient, daily_value in daily_values.items():
        if nutrient in product:
            try:
                product_value = safe_float_conversion(product[nutrient])
                percentage = round((product_value / daily_value) * 100, 2)
                percentages[nutrient] = percentage
            except Exception as e:
                st.warning(f"Could not calculate daily value for {nutrient}: {str(e)}")
                percentages[nutrient] = 0.0
    
    return percentages

def calculate_nutrient_ratios(product):
    ratios = {}
    
    try:
        protein = safe_float_conversion(product['protein'])
        carbs = safe_float_conversion(product['carbohydrates'])
        total_fat = safe_float_conversion(product['total_fat'])
        saturated_fat = safe_float_conversion(product['saturated_fat'])
        added_sugar = safe_float_conversion(product['added_sugar'])
        total_sugars = safe_float_conversion(product['total_sugars'])
        
        # Protein to Carb Ratio
        if carbs != 0:
            ratios['Protein to Carb Ratio'] = round(protein / carbs, 2)
        else:
            ratios['Protein to Carb Ratio'] = 'N/A (No carbs)'
        
        # Saturated to Unsaturated Fat Ratio
        unsaturated_fat = total_fat - saturated_fat
        if unsaturated_fat > 0:
            ratios['Saturated to Unsaturated Fat Ratio'] = round(saturated_fat / unsaturated_fat, 2)
        else:
            ratios['Saturated to Unsaturated Fat Ratio'] = 'N/A'
        
        # Added to Total Sugar Ratio
        if total_sugars > 0:
            ratios['Added to Total Sugar Ratio'] = round(added_sugar / total_sugars, 2)
        else:
            ratios['Added to Total Sugar Ratio'] = 'N/A (No sugars)'
            
    except Exce
