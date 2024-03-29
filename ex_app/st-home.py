import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
from snowflake.snowpark import Session
from pathlib import Path
from datetime import datetime  # For date and time
import pytz   
from st_pages import Page, add_page_title, show_pages

# Establish Snowflake session
st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(
    #page_title="Ex-stream-ly Cool App",
    #page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# display time start
# Get the timezone object
tz_NY = pytz.timezone('America/New_York') 
tz_IN = pytz.timezone('Asia/Kolkata') 
tz_LA = pytz.timezone('America/Los_Angeles') 

datetime_NY = datetime.now(tz_NY)
datetime_LA = datetime.now(tz_LA)
datetime_IN = datetime.now(tz_IN)

india_time = datetime_IN.strftime("%H:%M")
us_time = datetime_NY.strftime("%H:%M")
pst_time = datetime_LA.strftime("%H:%M")

c1, c2,c3 = st.columns([0.32,0.28,0.45])
with c1:
    st.write(f"> **⛄New York Time = {us_time}**")
with c2:
    st.write(f"> **☀️India Time = {india_time}**")
with c3:
    st.write(f"> **🌤️Los Angeles Time = {pst_time}**")

# display time end


st.divider()

c1, c2 = st.columns([1,2])
with c1:
 st.info('**💡 **Team Data Maverick**💡**')



def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()


 
 #st.info('**💡 Team Data Maverick 💡**', icon="💡")

    #"## Declaring the pages in your app:"
with st.expander("**Expand this area to read about Problem Statement**"):
    st.markdown("""
    **Problem Statement 1: Prediction & Anomaly Detection in Snowflake (Cortex)**

    **Ask**
   -  Choose a dataset of your choice (ex: Sales), load the data in Snowflake
   -  Create a model to forecast the demand (ex: for Products or Items)
   -  Augment additional data like Holiday, Weather etc and see if this improves the model.
   -  Perform trend analysis & identify anomalies
   -  Develop a Snowflake Streamlit App to showcase the workflow (inputs, process, output).
    
    **Over & Beyond**
   -  Async model retraining using Snowflake Tasks powered by Notifications via Email
   -  E2E Solution & Architecture Diagram (hand-drawn is fine too)
   -  Integrate with NLP to SQL

""")
st.divider()

st.title('Forecast Demand Visualization Application')

show_pages(
    [
        Page("ex_app/st-home.py", "Home", "🏠"),
            # Can use :<icon-name>: or the actual icon
        Page("ex_app/st-one.py", "Part One", "👖"),
            # The pages appear in the order you pass them
        Page("ex_app/st-two.py", "Part Two", ":shoe:"),
        Page("ex_app/st-three.py", "Part Three", "💰"),
        Page("ex_app/st-four.py", "Part Four", "💵"),
        Page("ex_app/st-five.py", "Part Five", "📉"),
            #Page("example_app/example_two.py", "Example Two", "✏️"),
            # Will use the default icon and name based on the filename if you don't
            # pass them
            #Page("example_app/example_three.py"),
            #Page("example_app/example_five.py", "Example Five", "🧰"),
    ]
)

add_page_title()  # Optional method to add title and icon to current page

st.markdown("""
This app will build **forecast model** adding holiday information & generate predictions for units sold, total sales & operating profit.
- Below is a sample Adidas sales dataset for the last 2 years consist of below products sold across **NYC** **:sun_with_face:**
    - **Men's Street Footwear**
    - **Men's Athletic Footwear**
    - **Men's Apparel**
* **Python libraries:** pandas, streamlit, matplotlib, altair
""")



def load_data(table_name):
    st.write(f"Here's some example data from `{table_name}`:")
    table = session.table(table_name)
    table = table.limit(20)
    table = table.collect()
    return table

table_name = "ADIDAS.PUBLIC.SALES_DATA"

col1,col2 = st.columns([2,1])

with col1:
 with st.expander("**View and Download data**"):
    df = load_data(table_name)
    st.dataframe(df)

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**💡 **Team Data Maverick**💡**')