import streamlit as st
from utils import calculate_bmi, bmi_category, calculate_daily_calories

def render_sidebar(df):
    with st.sidebar:
        # Page navigation at the bottom of the sidebar
        selected_page = st.selectbox(
            "Choose a page",
            ["Single Product Analysis", "Product Comparison", "Nutritional Guidelines"],
            key="page_selection"
        )
        st.header("Health Calculators")
        
        with st.expander("BMI Calculator"):
            render_bmi_calculator()
        
        with st.expander("Daily Calorie Calculator"):
            render_calorie_calculator()
        
        with st.expander("Nutrient Search"):
            render_nutrient_search(df)
        
        st.markdown("---")
     
        st.info("Developed with 🍩 by Team DotReview")
    
    return selected_page

def render_bmi_calculator():
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
    height = st.number_input("Height (cm)", min_value=1.0, max_value=300.0, value=170.0)
    if st.button("Calculate BMI"):
        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)
        st.write(f"Your BMI: {bmi}")
        st.write(f"Category: {category}")

def render_calorie_calculator():
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0, key="calorie_weight")
    height = st.number_input("Height (cm)", min_value=1.0, max_value=300.0, value=170.0, key="calorie_height")
    age = st.number_input("Age", min_value=1, max_value=120, value=30)
    gender = st.selectbox("Gender", ["Male", "Female"])
    activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])
    if st.button("Calculate Daily Calories"):
        daily_calories = calculate_daily_calories(weight, height, age, gender, activity)
        st.write(f"Estimated daily calorie needs: {daily_calories} kcal")

def render_nutrient_search(df):
    nutrient = st.selectbox("Select a nutrient", df.columns[1:])
    top_n = st.number_input("Number of top products", min_value=1, max_value=20, value=5)
    if st.button("Find Top Products"):
        top_products = df.nlargest(top_n, nutrient)[['name', nutrient]]
        st.table(top_products)
