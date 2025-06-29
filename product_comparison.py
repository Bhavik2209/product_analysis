import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def safe_float_conversion(value):
    """Safely convert a value to float, handling various input types."""
    try:
        if pd.isna(value) or value == '' or value is None:
            return 0.0
        return float(str(value).strip())
    except (ValueError, TypeError):
        return 0.0

def render(df):
    st.header("Product Comparison")
    
    col1, col2 = st.columns(2)
    with col1:
        product1_name = st.text_input('Enter the first product name:')
    with col2:
        product2_name = st.text_input('Enter the second product name:')
    
    if st.button('Compare'):
        product1 = df[df['name'].str.contains(product1_name, case=False, na=False)]
        product2 = df[df['name'].str.contains(product2_name, case=False, na=False)]
        
        if product1.empty or product2.empty:
            st.error("One or both products not found in the dataset.")
        else:
            product1 = product1.iloc[0]
            product2 = product2.iloc[0]
            
            try:
                comparison = compare_products(product1, product2)
                st.write("Product Comparison:")
                st.table(comparison)
                
                fig_comparison = px.bar(comparison, x='Nutrient', y=[product1['name'], product2['name']], 
                                        title=f"Comparison: {product1['name']} vs {product2['name']}",
                                        barmode='group')
                st.plotly_chart(fig_comparison)

                fig_radar = create_radar_chart(product1, product2)
                st.plotly_chart(fig_radar)

                winner, explanations = determine_better_product(product1, product2)
                st.subheader("Comparative Analysis")
                st.write(f"Based on our analysis, {winner} appears to be the better choice overall.")
                st.write("Here's why:")
                for explanation in explanations:
                    st.write(f"- {explanation}")

                st.write("Note: This analysis is based on a simplified comparison of key nutritional factors. "
                         "The 'better' product may vary depending on individual dietary needs and goals.")
                
            except Exception as e:
                st.error(f"Error during comparison: {str(e)}")

def compare_products(product1, product2):
    try:
        # Get numeric columns only (exclude 'name' column)
        numeric_columns = [col for col in product1.index if col != 'name']
        
        comparison_data = {
            'Nutrient': [],
            product1['name']: [],
            product2['name']: []
        }
        
        for nutrient in numeric_columns:
            try:
                val1 = safe_float_conversion(product1[nutrient])
                val2 = safe_float_conversion(product2[nutrient])
                
                comparison_data['Nutrient'].append(nutrient)
                comparison_data[product1['name']].append(val1)
                comparison_data[product2['name']].append(val2)
            except Exception as e:
                st.warning(f"Could not compare {nutrient}: {str(e)}")
        
        return pd.DataFrame(comparison_data)
    
    except Exception as e:
        st.error(f"Error creating comparison table: {str(e)}")
        return pd.DataFrame()

def create_radar_chart(product1, product2):
    try:
        categories = ['Energy', 'Protein', 'Carbs', 'Fiber', 'Total Fat', 'Saturated Fat', 'Added Sugar']
        nutrient_keys = ['energy_kcal', 'protein', 'carbohydrates', 'dietary_fiber', 'total_fat', 'saturated_fat', 'added_sugar']
        
        # Get values for product1
        values1 = []
        for key in nutrient_keys:
            values1.append(safe_float_conversion(product1[key]))
        
        # Get values for product2
        values2 = []
        for key in nutrient_keys:
            values2.append(safe_float_conversion(product2[key]))
        
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values1,
            theta=categories,
            fill='toself',
            name=product1['name']
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=values2,
            theta=categories,
            fill='toself',
            name=product2['name']
        ))

        # Calculate max value for scaling
        max_value = max(max(values1), max(values2))
        if max_value == 0:
            max_value = 1  # Avoid division by zero

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max_value * 1.1]  # Add 10% padding
                )),
            showlegend=True,
            title="Nutritional Radar Chart Comparison"
        )

        return fig
    
    except Exception as e:
        st.error(f"Error creating radar chart: {str(e)}")
        # Return empty figure
        return go.Figure()

def determine_better_product(product1, product2):
    try:
        scores = {product1['name']: 0, product2['name']: 0}
        explanations = []

        comparisons = [
            ('energy_kcal', 'fewer calories', 'lower'),
            ('protein', 'more protein', 'higher'),
            ('added_sugar', 'less added sugar', 'lower'),
            ('dietary_fiber', 'more dietary fiber', 'higher'),
            ('saturated_fat', 'less saturated fat', 'lower')
        ]

        for nutrient, explanation, preference in comparisons:
            try:
                val1 = safe_float_conversion(product1[nutrient])
                val2 = safe_float_conversion(product2[nutrient])
                
                if preference == 'lower':
                    if val1 < val2:
                        winner_name = product1['name']
                        scores[winner_name] += 1
                    elif val2 < val1:
                        winner_name = product2['name']
                        scores[winner_name] += 1
                    else:
                        continue  # It's a tie for this nutrient
                else:  # preference == 'higher'
                    if val1 > val2:
                        winner_name = product1['name']
                        scores[winner_name] += 1
                    elif val2 > val1:
                        winner_name = product2['name']
                        scores[winner_name] += 1
                    else:
                        continue  # It's a tie for this nutrient
                
                explanations.append(f"{winner_name} has {explanation}")
                
            except Exception as e:
                st.warning(f"Could not compare {nutrient}: {str(e)}")

        # Determine overall winner
        if scores[product1['name']] > scores[product2['name']]:
            winner = product1['name']
        elif scores[product2['name']] > scores[product1['name']]:
            winner = product2['name']
        else:
            winner = "It's a tie"
        
        return winner, explanations
    
    except Exception as e:
        st.error(f"Error determining better product: {str(e)}")
        return "Unable to determine", ["Error in analysis"]
