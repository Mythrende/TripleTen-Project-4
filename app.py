# app.py
import os
import pandas as pd
import streamlit as st
import plotly.express as px

# -------------------------------
# Load CSV
# -------------------------------
csv_path = os.path.join(os.path.dirname(__file__), "vehicles_us.csv")
vehicles = pd.read_csv(csv_path)

# -------------------------------
# Handle Missing Values
# -------------------------------
vehicles['model_year'] = vehicles['model_year'].fillna(0)
vehicles['type'] = vehicles['type'].astype(str)
vehicles['cylinders'] = vehicles['cylinders'].fillna(vehicles.groupby('type')['cylinders'].transform('median'))
vehicles['odometer'] = vehicles['odometer'].fillna(vehicles.groupby('type')['odometer'].transform('median'))
vehicles['paint_color'] = vehicles['paint_color'].fillna('Unknown')
vehicles['is_4wd'] = vehicles['is_4wd'].fillna(0)

# -------------------------------
# Convert Data Types
# -------------------------------
vehicles['price'] = vehicles['price'].astype(float)
vehicles['model_year'] = vehicles['model_year'].astype('Int64')
vehicles['model'] = vehicles['model'].astype(str)
vehicles['condition'] = vehicles['condition'].astype(str)
vehicles['cylinders'] = vehicles['cylinders'].astype('Int64')
vehicles['fuel'] = vehicles['fuel'].astype(str)
vehicles['odometer'] = vehicles['odometer'].astype(float)
vehicles['transmission'] = vehicles['transmission'].astype(str)
vehicles['type'] = vehicles['type'].astype(str)
vehicles['paint_color'] = vehicles['paint_color'].astype(str)
vehicles['is_4wd'] = vehicles['is_4wd'].astype('Int64')
vehicles['date_posted'] = pd.to_datetime(vehicles['date_posted'])
vehicles['days_listed'] = vehicles['days_listed'].astype('Int64')

# -------------------------------
# Rename Columns
# -------------------------------
vehicles = vehicles.rename(columns={
    "price": "Price",
    "model_year": "Model Year",
    "model": "Model",
    "condition": "Condition",
    "cylinders": "Cylinders",
    "fuel": "Fuel",
    "odometer": "Odometer",
    "transmission": "Transmission",
    "type": "Type",
    "paint_color": "Paint Color",
    "is_4wd": "Is 4WD",
    "date_posted": "Date Posted",
    "days_listed": "Days Listed"
})

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.title("Vehicle Sales Analysis")
st.header("How Each Attribute Affects a Car's Selling Price")

# -------------------------------
# Scatter Plot Section
# -------------------------------
plot_one = st.checkbox('Show Scatter Plot', value=True, key="scatter_checkbox")

if plot_one:
    genre = st.radio(
        "Choose Which Attribute You Want to use as the X-Axis",
        ["Cylinders", "Model Year", "Condition"],
        index=0,
        horizontal=True,
        key="scatter_radio"
    )

    values = st.slider(
        'Select Model Years of Interest (0 = Unknown)',
        0, 2020, (0, 2020),
        key="scatter_slider"
    )

    vehicles_filtered = vehicles[vehicles["Model Year"].between(values[0], values[1])]

    fig_one = px.scatter(
        vehicles_filtered,
        x=genre,
        y="Price",
        color="Condition",
        symbol="Condition",
        hover_data=['Model'],
        title=f"Scatter Plot of {genre} vs. Price",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    st.plotly_chart(fig_one, theme="streamlit", use_container_width=True)

# -------------------------------
# Histogram Section
# -------------------------------
plot_two = st.checkbox('Show Histogram', value=True, key="hist_checkbox")

if plot_two:
    option = st.selectbox(
        "Select attribute to color by in the histogram",
        ('Type', 'Paint Color', 'Transmission', 'Condition'),
        key="hist_selectbox"
    )

    values_two = st.slider(
        'Select Model Years of Interest (0 = Unknown)',
        0, 2020, (0, 2020),
        key="hist_slider"
    )

    vehicles_filtered = vehicles[vehicles["Model Year"].between(values_two[0], values_two[1])]

    fig_two = px.histogram(
        vehicles_filtered,
        x="Model Year",
        color=option,
        title=f"Histogram of Model Year vs. {option}",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )

    st.plotly_chart(fig_two, theme="streamlit", use_container_width=True)