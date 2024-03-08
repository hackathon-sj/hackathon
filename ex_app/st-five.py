import streamlit as st
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
from snowflake.snowpark import Session
from st_pages import add_page_title
from datetime import datetime  # For date and time
import pytz   

#add_page_title(layout="wide")

# Establish Snowflake session
st.cache_data.clear()
st.cache_resource.clear()


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


st.header('💵:shoe:👖 **Part Five-Anomaly Detection**')
st.subheader('**Anomalous Sales based on Units Sold**')

def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()

c1, c2 = st.columns([1,2])
with c1:
 st.info('**💡 **Team Data Maverick**💡**')

st.divider()
       

st.write('✏️ **Step 1:- Create Anamoly Detection model for **:green[units sold]****')

if 'button_clicked7' not in st.session_state:
    st.session_state.button_clicked7 = False
if st.button("**:blue[Create Anamoly Detection Model!]**"):
    st.session_state.button_clicked7=True
    session.sql("CREATE OR REPLACE snowflake.ml.anomaly_detection ADIDAS.PUBLIC.us_anomaly_model(INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.us_anomaly_training_set'),SERIES_COLNAME => 'PRODUCT',TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'UNITS_SOLD', LABEL_COLNAME => ''); ;").collect()

if st.session_state.button_clicked7:
    st.success("Anamoly Detection Model created successfully !")

st.write('✏️ **Step 2:- Detect Anamolies for **:green[units sold]** for the prediction interval selected by user**')
Interval = st.selectbox(
     '**:red[Select Prediction Interval]**',
     ('0.85', '0.90', '0.95'),help="Train model to create predictions for the demand for the selected days")

st.write('**Selected Prediction Interval:**', Interval)

if 'button_clicked8' not in st.session_state:
    st.session_state.button_clicked8 = False
if st.button("**:blue[Detect Anamolies !]**"):
    st.session_state.button_clicked8=True
    session.sql("CALL ADIDAS.PUBLIC.us_anomaly_model!DETECT_ANOMALIES(INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.us_anomaly_analysis_set'),SERIES_COLNAME => 'PRODUCT',TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'UNITS_SOLD',CONFIG_OBJECT => {'prediction_interval': 0.95});").collect()
    session.sql("CREATE OR REPLACE TABLE ADIDAS.PUBLIC.us_anomalies AS (SELECT * FROM TABLE(RESULT_SCAN(-1)));").collect()
if st.session_state.button_clicked8:
    st.success("Anamolies Detected successfully !")

st.write('✏️ **Step 3:- Create Visualization**')
if 'button_clicked9' not in st.session_state:
    st.session_state.button_clicked9 = False
if st.button("**:blue[View Line Chart!]**"):
    st.session_state.button_clicked9=True



st.write(":heavy_minus_sign:" * 29)       
 


st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**💡 **Team Data Maverick**💡**')