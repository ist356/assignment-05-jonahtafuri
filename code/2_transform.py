import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here
# Load the states and survey data from the cache into dataframes. `states_data` and `survey_data`
# create a unique list of years from the survey data
# For each year in the survey data, load the cost of living data from the cache into a dataframe, 
# then combine all the dataframes into a single cost of living (COL) dataframe `col_data`

# First, clean the entry under "Which country do you work in?" so that all US countries say "United States" use the `clean_country_usa` function in `pandaslib.py` function here and generate a new column `_country`
# Next under the "If you're in the U.S., what state do you work in?" column we need to convert the states into state codes Example: "New York => NY" to do this, join the states dataframe to the survey dataframe. User and inner join to drop non-matches. Call the new dataframe `survey_states_combined`
# Engineer a new column consisting of the city, a comma, the 2-character state abbreviation, another comma and `_country` For example: "Syracuse, NY, United States". name this column `_full_city`
# create the dataframe `combined` by matching the `survey_states_combined` to cost of living data matching on the `year` and `_full_city` columns

# Clean the salary column so that its a float. Use `clean_currency` function in `pandaslib.py`. generate a new column `__annual_salary_cleaned`
# generate a column `_annual_salary_adjusted` based on this formula. 

state_data = pd.read_csv('cache/states.csv')
survey_data = pd.read_csv('cache/salaries.csv')
years = survey_data['year'].unique()
df_list = []
for year in years:
    col_year = pd.read_csv(f'cache/col_{year}.csv')
    # st.dataframe(col_year)
    col_year['year'] = year
    df_list.append(col_year)
col_data = pd.concat(df_list)

st.dataframe(survey_data)
survey_data['_country'] = survey_data['What country do you work in?'].apply(pl.clean_country_usa)

survey_states_combined = survey_data.merge(state_data, left_on='If you\'re in the U.S., what state do you work in?', right_on='State', how='inner')

## create a new column _full_city example: "Syracuse, NY, United States"
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['_country']
# st.write("survey_states_combined full city")
# st.dataframe(survey_states_combined['_full_city'])
combined = survey_states_combined.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')
combined['_annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
# st.dataframe(combined)
combined['_annual_salary_adjusted'] = combined.apply(lambda row: row["_annual_salary_cleaned"] * (100 / row['Cost of Living Index']), axis=1)

combined.to_csv(f'cache/survey_dataset.csv', index=False)

# create the first report to show a pivot table of the the average `_annual_salary_adjusted` with `_full_city` in the row and Age band (How old are you?) in the column. Save this back to the cache as `annual_salary_adjusted_by_location_and_age.csv`
# create a similar report but show highest level of education in the column. Save this back to the cache as `annual_salary_adjusted_by_location_and_education.csv`
# student_responses = merged_df.groupby(['netid', 'date'])['answer'].count().unstack(fill_value=0)
annual_salary_adjusted_by_location_and_age = combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean')
annual_salary_adjusted_by_location_and_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')
st.write("Annual Salary adjusted by location and age")
st.dataframe(annual_salary_adjusted_by_location_and_age)

annual_salary_adjusted_by_location_and_education = combined.pivot_table(index='_full_city', columns='What is your highest level of education completed?', values='_annual_salary_adjusted', aggfunc='mean')
annual_salary_adjusted_by_location_and_education.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')
st.write("Annual Salary adjusted by location and education")
st.dataframe(annual_salary_adjusted_by_location_and_education)
