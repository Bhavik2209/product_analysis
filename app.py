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
        st.error("An unexpected error occurred. Please try again later.")

if __name__ == "__main__":
    main()
