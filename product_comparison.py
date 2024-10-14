import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

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

def compare_products(product1, product2):
    return pd.DataFrame({
        'Nutrient': product1.index[1:],
        product1['name']: product1.values[1:],
        product2['name']: product2.values[1:]
    })

def create_radar_chart(product1, product2):
    categories = ['Energy', 'Protein', 'Carbs', 'Fiber', 'Total Fat', 'Saturated Fat', 'Added Sugar']
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[product1['energy_kcal'], product1['protein'], product1['carbohydrates'], 
           product1['dietary_fiber'], product1['total_fat'], product1['saturated_fat'], 
           product1['added_sugar']],
        theta=categories,
        fill='toself',
        name=product1['name']
    ))
    fig.add_trace(go.Scatterpolar(
        r=[product2['energy_kcal'], product2['protein'], product2['carbohydrates'], 
           product2['dietary_fiber'], product2['total_fat'], product2['saturated_fat'], 
           product2['added_sugar']],
        theta=categories,
        fill='toself',
        name=product2['name']
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(product1['energy_kcal'], product2['energy_kcal'])]
            )),
        showlegend=True
    )

    return fig

def determine_better_product(product1, product2):
    scores = {product1['name']: 0, product2['name']: 0}
    explanations = []

    comparisons = [
        ('energy_kcal', 'fewer calories', min),
        ('protein', 'more protein', max),
        ('added_sugar', 'less added sugar', min),
        ('dietary_fiber', 'more dietary fiber', max),
        ('saturated_fat', 'less saturated fat', min)
    ]

    for nutrient, explanation, compare_func in comparisons:
        better_product = compare_func(product1, product2, key=lambda x: x[nutrient])
        scores[better_product['name']] += 1
        explanations.append(f"{better_product['name']} has {explanation}.")

    winner = max(scores, key=scores.get) if scores[product1['name']] != scores[product2['name']] else "It's a tie"  
    return winner, explanations