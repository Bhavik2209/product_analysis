# utils.py
import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import logging

# Load environment variables
GOOGLE_API_KEY = st.secrets['default']['GOOGLE_API_KEY']
# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dotReview_data.csv")
        df.columns = ['name', 'energy_kcal', 'protein', 'carbohydrates', 'total_sugars', 'added_sugar', 
                      'dietary_fiber', 'trans_fat', 'saturated_fat', 'total_fat', 'cholesterol_mg', 
                      'sodium_mg', 'iron_mg', 'calcium_mg', 'ingredient_1', 'ingredient_2', 'ingredient_3', 
                      'ingredient_4', 'ingredient_5', 'ingredient_6', 'ingredient_7', 'ingredient_8', 
                      'ingredient_9','ingredient_10','ingredient_11','ingredient_12']
        return df.drop(columns=['ingredient_1', 'ingredient_2', 'ingredient_3', 'ingredient_4', 
                                'ingredient_5', 'ingredient_6', 'ingredient_7', 'ingredient_8', 
                                'ingredient_9','ingredient_10','ingredient_11','ingredient_12'])
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        st.error("Error loading data. Please check if the data file exists and is accessible.")
        return None

def calculate_bmi(weight, height):
    bmi = weight / (height/100)**2
    return round(bmi, 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_daily_calories(weight, height, age, gender, activity_level):
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    activity_factors = {
        'sedentary': 1.2,
        'lightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'extra active': 1.9
    }
    
    return round(bmr * activity_factors[activity_level.lower()], 2)

def generate_nutritional_insights(product):
    prompt = f"""
    Analyze the following nutritional information and provide insights:
    Product: {product['name']}
    Energy: {product['energy_kcal']} kcal
    Protein: {product['protein']} g
    Carbohydrates: {product['carbohydrates']} g
    Total Sugars: {product['total_sugars']} g
    Added Sugar: {product['added_sugar']} g
    Dietary Fiber: {product['dietary_fiber']} g
    Total Fat: {product['total_fat']} g
    Saturated Fat: {product['saturated_fat']} g
    Trans Fat: {product['trans_fat']} g
    Cholesterol: {product['cholesterol_mg']} mg
    Sodium: {product['sodium_mg']} mg
    Iron: {product['iron_mg']} mg
    Calcium: {product['calcium_mg']} mg

    Provide a detailed analysis of the nutritional content, highlighting any potential health benefits or concerns. 
    Compare the values to daily recommended intakes and suggest improvements if necessary.
    Structure your response in the following format:
    1. Overall Nutritional Profile
    2. Macronutrients Analysis
    3. Micronutrients Analysis
    4. Potential Health Benefits
    5. Areas of Concern
    6. Recommendations for Improvement
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Error generating nutritional insights: {str(e)}")
        return "Unable to generate nutritional insights at this time. Please try again later."
