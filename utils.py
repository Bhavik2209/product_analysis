# utils.py
import streamlit as st
import pandas as pd
import os
import logging

# Import LangChain and relevant LLM
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

import getpass
import os

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = st.secrets['default']['GROQ_API_KEY']
# Load environment variables
GROQ_API_KEY = st.secrets['default']['GROQ_API_KEY']

# Setup LangChain LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

@st.cache_data
def load_data():
    try:
        # Try multiple encodings to handle the file properly
        encodings_to_try = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        df = None
        for encoding in encodings_to_try:
            try:
                logging.info(f"Attempting to read CSV with {encoding} encoding...")
                df = pd.read_csv("dotReview_data_updated.csv", encoding=encoding)
                logging.info(f"Successfully loaded data with {encoding} encoding")
                break
            except UnicodeDecodeError as e:
                logging.warning(f"Failed to read with {encoding} encoding: {str(e)}")
                continue
            except Exception as e:
                logging.error(f"Error reading CSV with {encoding} encoding: {str(e)}")
                continue
        
        if df is None:
            raise Exception("Could not read CSV file with any of the attempted encodings")
        
        # Set column names
        df.columns = ['name', 'energy_kcal', 'protein', 'carbohydrates', 'total_sugars', 'added_sugar', 
                      'dietary_fiber', 'trans_fat', 'saturated_fat', 'total_fat', 'cholesterol_mg', 
                      'sodium_mg', 'iron_mg', 'calcium_mg', 'ingredient_1', 'ingredient_2', 'ingredient_3', 
                      'ingredient_4', 'ingredient_5', 'ingredient_6', 'ingredient_7', 'ingredient_8', 
                      'ingredient_9','ingredient_10','ingredient_11','ingredient_12']
        
        # Drop ingredient columns
        df_cleaned = df.drop(columns=['ingredient_1', 'ingredient_2', 'ingredient_3', 'ingredient_4', 
                                'ingredient_5', 'ingredient_6', 'ingredient_7', 'ingredient_8', 
                                'ingredient_9','ingredient_10','ingredient_11','ingredient_12'])
        
        logging.info(f"Data loaded successfully. Shape: {df_cleaned.shape}")
        return df_cleaned
        
    except FileNotFoundError:
        logging.error("CSV file 'dotReview_data_updated.csv' not found")
        st.error("Data file not found. Please ensure 'dotReview_data_updated.csv' exists in the project directory.")
        return pd.DataFrame()  # Return empty DataFrame instead of None
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")
        st.error(f"Error loading data: {str(e)}. Please check if the data file exists and is accessible.")
        return pd.DataFrame()  # Return empty DataFrame instead of None

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
    template = """
    Analyze the following nutritional information and provide insights:
    Product: {name}
    Energy: {energy_kcal} kcal
    Protein: {protein} g
    Carbohydrates: {carbohydrates} g
    Total Sugars: {total_sugars} g
    Added Sugar: {added_sugar} g
    Dietary Fiber: {dietary_fiber} g
    Total Fat: {total_fat} g
    Saturated Fat: {saturated_fat} g
    Trans Fat: {trans_fat} g
    Cholesterol: {cholesterol_mg} mg
    Sodium: {sodium_mg} mg
    Iron: {iron_mg} mg
    Calcium: {calcium_mg} mg

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
    
    required_keys = [
        "name", "energy_kcal", "protein", "carbohydrates", "total_sugars", "added_sugar",
        "dietary_fiber", "total_fat", "saturated_fat", "trans_fat", "cholesterol_mg",
        "sodium_mg", "iron_mg", "calcium_mg"
    ]
    
    try:
        # Format the prompt
        prompt = PromptTemplate(
            input_variables=required_keys,
            template=template
        )
        prompt_filled = prompt.format(**product)

        # Generate response
        logging.info("Sending prompt to LangChain...")
        response = llm.invoke(prompt_filled)
        logging.info("Received response from LangChain.")
        return response.content
    except Exception as e:
        logging.error(f"Error generating nutritional insights: {str(e)}")
        return "Unable to generate nutritional insights at this time. Please try again later."
