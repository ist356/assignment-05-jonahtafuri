import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl


# - For each file you extract save it in `.csv` format with a header to the `cache` folder. The basic process is to read the file, add lineage, then write as a `.csv` to the `cache` folder. 
# - Extract the states with codes google sheet. Save as `cache/states.csv`
# - Extract the survey google sheet, and engineer a `year` column from the `Timestamp` using the `extract_year_mdy` function in `pandaslib.py`. Then save as `cache/survey.csv`
# - For each unique year in the surveys: extract the cost of living for that year from the website, engineer a `year` column for that year, then save as `cache/col_{year}.csv` for example for `2024` it would be `cache/col_2024.csv`
#TODO Write your extraction code here

# extract files from webpage
states = pd.read_csv("https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv")
salaries = pd.read_csv("https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv")

salaries['year'] = salaries['Timestamp'].apply(pl.extract_year_mdy)
st.write("OUTPUT:", salaries['year'].unique())

# write salaries to the cache as a csv
salaries_years = salaries['year'].unique()
for year in salaries_years:
    col_year = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    col_year = col_year[1]
    col_year['year'] = year
    col_year.to_csv(f'cache/col_{year}.csv', index=False)

    
salaries.to_csv("cache/salaries.csv", index=False)
states.to_csv("cache/states.csv", index=False)


# st.dataframe(state_abrevs.head())
st.dataframe(salaries)
st.dataframe(states)

