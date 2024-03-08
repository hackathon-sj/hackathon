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


st.header('💵:shoe:👖 **Part Four-Forecasting Demand**')
st.subheader('**Total Sales for Multiple Products including Holidays**')
st.markdown("""- Men\'s Apparel
- Men\'s Athletic Footwear 
- Men\'s Street Footwear""")


def create_session():
    return Session.builder.configs(st.secrets["snowflake"]).create()

session = create_session()

c1, c2 = st.columns([1,2])
with c1:
 st.info('**💡 **Team Data Maverick**💡**')

st.divider()

def make_heatmap3 ():
    
 # Assuming 'df' is a pandas DataFrame with 'TIMESTAMP', 'TOTAL_SALES_$', and 'FORECAST' columns
    df = session.sql("SELECT timestamp as timestamp, total_sales, product, NULL AS forecast FROM ADIDAS.PUBLIC.ALLPRODUCTS_total_SALES where to_date(timestamp ) > (SELECT max(to_date(timestamp)) - interval ' 2 months' FROM ADIDAS.PUBLIC.ALLPRODUCTS_total_SALES) UNION SELECT TS AS timestamp, NULL AS total_sales, series AS product, forecast FROM ADIDAS.PUBLIC.us_total_sales_predictions ORDER BY timestamp, product asc").to_pandas()

    # Creating line charts for Units Sold and Forecast
    line_total_sales = alt.Chart(df).mark_line(color='blue', size=2).encode(
        x='TIMESTAMP:T',
        y='TOTAL_SALES:Q',
        tooltip=['TIMESTAMP', 'TOTAL_SALES']
    ).properties(
        title='Total Sales'
    )

    line_forecast = alt.Chart(df).mark_line(color='yellow', size=2).encode(
        x='TIMESTAMP:T',
        y='FORECAST:Q',
        tooltip=['TIMESTAMP', 'FORECAST']
    ).properties(
        title='Forecast'
    )

    # Combine the charts
    chart3 = alt.layer(line_total_sales, line_forecast).resolve_scale(
        y='independent'
    ).properties(
        title='Total Sales Forecast Visualization',
        width='container',
        height=300  # You can adjust the height as needed
    )

    return chart3

       

#st.markdown("""
#- Third part will generate forecasting model for total sales for only one product- **Men's Apparel**.
#- Since we have sales dataset till 31-Jan-2024,it will generate predictions for units sold for the number of days selected by user.
#- Finally we will generate visualizations in the form of line chart.
#""")

st.write('✏️ **Step 1:- Create Forecasting model for **:green[total sales]** for multiple products- **:orange[Men\'s Apparel,Men\'s Athletic Footwear & Men\'s Street Footwear]****')

if 'button_clicked7' not in st.session_state:
    st.session_state.button_clicked7 = False
if st.button("**:blue[Create Forecasting Model!]**"):
    st.session_state.button_clicked7=True
    session.sql("CREATE OR REPLACE forecast ADIDAS.PUBLIC.allproducts_sales_forecast (INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.ALLPRODUCTS_total_SALES'),SERIES_COLNAME => 'PRODUCT',TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'TOTAL_SALES');").collect()

if st.session_state.button_clicked7:
    st.success("Forecasting Model created successfully !")

st.write('✏️ **Step 2:- Create Predictions for **:green[total sales]** for the number of days selected by user**')
Days = st.selectbox(
     '**:red[Select Forecasting Period]**',
     ('30', '60', '90'),help="Train model to create predictions for the demand for the selected days")

st.write('**Selected days:**', Days)

if 'button_clicked8' not in st.session_state:
    st.session_state.button_clicked8 = False
if st.button("**:blue[Create Predictions!]**"):
    st.session_state.button_clicked8=True
    session.sql("CREATE OR REPLACE VIEW ADIDAS.PUBLIC.us_forecast_data_sales AS (WITH future_dates AS (SELECT (select max(timestamp) from NY_SALES_DATA) ::DATE + row_number() OVER (ORDER BY 0) AS timestamp FROM TABLE(generator(rowcount => "+Days+"))),product_items AS (select distinct product  from ALLPRODUCTS_total_SALES),joined_product_items AS (SELECT * FROM product_items CROSS JOIN future_dates ORDER BY product ASC, timestamp ASC)SELECT jmi.product,to_timestamp_ntz(jmi.timestamp) AS timestamp,ch.holiday_name FROM joined_product_items AS jmi LEFT JOIN us_holidays ch ON jmi.timestamp = ch.date ORDER BY jmi.product ASC,jmi.timestamp ASC);").collect()
    session.sql("CALL ADIDAS.PUBLIC.allproducts_sales_forecast!forecast(INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.us_forecast_data_sales'),SERIES_COLNAME => 'product',TIMESTAMP_COLNAME => 'timestamp');").collect()
    session.sql("CREATE OR REPLACE TABLE ADIDAS.PUBLIC.us_total_sales_predictions AS (SELECT * FROM TABLE(RESULT_SCAN(-1)));").collect()
if st.session_state.button_clicked8:
    st.success("Predictions created successfully !")

st.write('✏️ **Step 3:- Create Visualization**')
if 'button_clicked9' not in st.session_state:
    st.session_state.button_clicked9 = False
if st.button("**:blue[View Line Chart!]**"):
    st.session_state.button_clicked9=True



st.write(":heavy_minus_sign:" * 29)       
 
heatmap_chart3 = make_heatmap3()
if st.session_state.button_clicked9:
    st.altair_chart(heatmap_chart3, use_container_width=True)
    st.success("Visualization created")

st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**💡 **Team Data Maverick**💡**')