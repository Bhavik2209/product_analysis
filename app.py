# main.py
import streamlit as st
import single_product, product_comparison, nutritional_guidelines
from sidebar import render_sidebar
from utils import load_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        st.set_page_config(page_title="Nutritional Analysis App", page_icon="🍎", layout="wide")
        st.title('DotReview - Food Products Analysis')

        # Load data
        df = load_data()
        
        # Check if data was loaded successfully
        if df is None or df.empty:
            st.error("Failed to load data. Please check if the CSV file exists and is properly formatted.")
            st.info("Please ensure 'dotReview_data_updated.csv' is in the project directory and contains valid data.")
            return

        # Display data info for debugging
        logging.info(f"Data loaded successfully. Shape: {df.shape}, Columns: {list(df.columns)}")

        # Render sidebar and get selected page
        selected_page = render_sidebar(df)

        # Render selected page
        if selected_page == "Single Product Analysis":
            single_product.render(df)
        elif selected_page == "Product Comparison":
            product_comparison.render(df)
        elif selected_page == "Nutritional Guidelines":
            nutritional_guidelines.render()

        logging.info(f"User navigated to {selected_page}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        st.error(f"An unexpected error occurred: {str(e)}")
        st.info("Please check the logs for more details and ensure all required files are present.")

if __name__ == "__main__":
    main()
