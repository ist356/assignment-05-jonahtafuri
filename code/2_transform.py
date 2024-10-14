import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
# Load the states and survey data from the cache into dataframes. `states_data` and `survey_data`
# create a unique list of years from the survey data
# For each year in the survey data, load the cost of living data from the cache into a dataframe, 
# then combine all the dataframes into a single cost of living (COL) dataframe `col_data`

state_data = pd.read_csv('cache/states.csv')
survey_data = pd.read_csv('cache/salaries.csv')
years = survey_data['year'].unique()
df_list = []
st.write("Years:", years)
for year in years:
    col_year = pd.read_csv(f'cache/col_{year}.csv')
    # st.dataframe(col_year)
    col_year['year'] = year
    df_list.append(col_year)
col_data = pd.concat(df_list)

# st.dataframe(col_data)