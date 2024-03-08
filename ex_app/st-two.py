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



st.header(':shoe:👖 **Part Two-Forecasting Demand**')
st.subheader('**Units Sold for Multiple Products including Holidays**')
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

def make_chart ():
    #df = session.sql("SELECT to_date(timestamp)as timestamp, units_sold, product, NULL AS forecast FROM ADIDAS.PUBLIC.allproducts_sales where to_date(timestamp ) > (SELECT max(to_date(timestamp)) - interval ' 1 months' FROM ADIDAS.PUBLIC.allproducts_sales) UNION SELECT to_date(TS) AS timestamp, NULL AS units_sold, series AS product, forecast FROM ADIDAS.PUBLIC.us_sales_predictions ORDER BY timestamp, product asc").to_pandas()
    df = session.sql("SELECT timestamp as timestamp, units_sold, product, NULL AS forecast FROM ADIDAS.PUBLIC.allproducts_sales where to_date(timestamp ) > (SELECT max(to_date(timestamp)) - interval ' 2 months' FROM ADIDAS.PUBLIC.allproducts_sales) UNION SELECT TS AS timestamp, NULL AS units_sold, series AS product, forecast FROM ADIDAS.PUBLIC.us_sales_predictions ORDER BY timestamp, product asc").to_pandas()
        
    
# Altair tooltip for interactive exploration
    tooltip = [alt.Tooltip('TIMESTAMP:T', title='TIMESTAMP'),
                alt.Tooltip('PRODUCT:N', title='PRODUCT'),
                alt.Tooltip('UNITS_SOLD:Q', title='UNITS SOLD'),
                alt.Tooltip('FORECAST:Q', title='FORECAST')]
# Create a base chart with common encoding
    base = alt.Chart(df).encode(
            alt.X('TIMESTAMP:T', title='TIMESTAMP'),
            alt.Color('PRODUCT:N', legend=alt.Legend(title="Product"))
         ).properties(
            width='container'
         )
         
# Define the units sold line
    units_sold_line = base.mark_line().encode(
            alt.Y('UNITS_SOLD:Q', title='UNITS_SOLD', scale=alt.Scale(zero=False)),
            tooltip=tooltip
        )
# Define the forecast line
    forecast_line = base.mark_line(strokeDash=[5,5]).encode(
            alt.Y('FORECAST:Q', scale=alt.Scale(zero=False)),
            tooltip=tooltip
        )
# Combine the charts
        #chart = alt.layer(units_sold_line, forecast_line).resolve_scale(y='independent')
        #chart = alt.layer( forecast_line).resolve_scale(y='independent')
    chart = alt.layer(units_sold_line, forecast_line
    ).properties(
        title='Units Sold for all 3 products-Forecast Visualization',
        width='container',
        height=300  # You can adjust the height as needed
    ).interactive()
        #chart.grid(True)
        #chart.legend()
    st.session_state.chart = chart
    return st.session_state.chart


# Sidebar for actions


st.write('✏️ **Step 1:- Create Forecasting model for **:green[units sold]** for multiple products- **:orange[Men\'s Apparel,Men\'s Athletic Footwear & Men\'s Street Footwear]****')

if 'button_clicked4' not in st.session_state:
    st.session_state.button_clicked4 = False
if st.button("**:blue[Create Forecasting Model!]**"):
        # Build Forecasting Model logic here
    st.session_state.button_clicked4=True
    session.sql("CREATE OR REPLACE forecast ADIDAS.PUBLIC.allproducts_forecast (INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.allproducts_sales'),SERIES_COLNAME => 'PRODUCT',TIMESTAMP_COLNAME => 'TIMESTAMP',TARGET_COLNAME => 'UNITS_SOLD');").collect()
if st.session_state.button_clicked4:
    st.success("Forecasting Model created successfully !")

st.write('✏️ **Step 2:- Create Predictions for **:green[units sold]** for the number of days selected by user**')
Days = st.selectbox(
     '**:red[Select Forecasting Period]**',
     ('30', '60', '90'),help="Train model to create predictions for the demand for the selected days")

st.write('**Selected days:**', Days)


if 'button_clicked5' not in st.session_state:
    st.session_state.button_clicked5 = False
if st.button("**:blue[Create Predictions!]**"):
        # Generate Predictions logic here
    st.session_state.button_clicked5=True
    session.sql("CREATE OR REPLACE VIEW ADIDAS.PUBLIC.us_forecast_data AS (WITH future_dates AS (SELECT (select max(timestamp) from NY_SALES_DATA) ::DATE + row_number() OVER (ORDER BY 0) AS timestamp FROM TABLE(generator(rowcount => "+Days+"))),product_items AS (select distinct product  from allproducts_sales),joined_product_items AS (SELECT * FROM product_items CROSS JOIN future_dates ORDER BY product ASC, timestamp ASC)SELECT jmi.product,to_timestamp_ntz(jmi.timestamp) AS timestamp,ch.holiday_name FROM joined_product_items AS jmi LEFT JOIN us_holidays ch ON jmi.timestamp = ch.date ORDER BY jmi.product ASC,jmi.timestamp ASC);").collect()
    session.sql("CALL ADIDAS.PUBLIC.allproducts_forecast!forecast(INPUT_DATA => SYSTEM$REFERENCE('VIEW', 'ADIDAS.PUBLIC.us_forecast_data'),SERIES_COLNAME => 'product',TIMESTAMP_COLNAME => 'timestamp');").collect()
    session.sql("CREATE OR REPLACE TABLE ADIDAS.PUBLIC.us_sales_predictions AS (SELECT * FROM TABLE(RESULT_SCAN(-1)));").collect()
if st.session_state.button_clicked5:
    st.success("Predictions created successfully !")

st.write('✏️ **Step 3:- Create Visualization**')
if 'button_clicked6' not in st.session_state:
    st.session_state.button_clicked6 = False
if st.button("**:blue[View Line Chart!]**"):
        # Generate Visualizations logic for col6 here
        # Visualization logic here (use fit-to-screen mode)
    st.session_state.button_clicked6=True
    #st.write(":heavy_minus_sign:" * 29)    
 
#col = st.columns((1.5, 4.5, 2), gap='medium')




st.write(":heavy_minus_sign:" * 29)    

chart1= make_chart()
if st.session_state.button_clicked6:
    st.altair_chart(chart1, use_container_width=True)
        
        #st.pyplot(heatmap,use_container_width=True)
    st.success("Visualization created finally")


st.divider()

c1, c2, c3 = st.columns(3)
with c1:
    st.info('**💡 **Team Data Maverick**💡**')