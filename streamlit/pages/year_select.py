
import streamlit as st
import pandas as pd
import numpy as np
import json
import gcsfs
import requests
import os
def open_from_bucket():
    gcs_file_system = gcsfs.GCSFileSystem()
    gcs_json_path = "gs://law-data-ogiles/data/simplified_data.json"
    with gcs_file_system.open(gcs_json_path) as f:
        json_dict = json.load(f)
    data = eval(json_dict)
    clean_data = [case for case in data if not case["press summary"].get('error')]
    new_data = clean_data[8:40] + clean_data[104:894]
    return new_data

def get_year(date):
    new_date = date[-4:]
    return new_date

data_df = pd.DataFrame(open_from_bucket())
details_list = list(data_df['details'])
details_df = pd.DataFrame(details_list)
year_dir = details_df.drop(columns=['Case ID', 'Neutral citation', 'Justices'])
year_dir['Year'] = year_dir['Judgment date'].map(get_year)
years = year_dir['Year'].unique()

questions_df = pd.DataFrame({'questions': ['Please select', 'Sample Question 1', 'Sample Question 2']})

base_path = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.dirname(base_path)
path = os.path.join(base_path, 'data', 'summarised_data.json')
with open(path, 'r') as myfile:
    data=myfile.read()
obj = json.loads(data)
data_dictionary_summarised = obj

def app():
    st.title('Translate the Law')
    st.write('##')
    st.subheader('Select a case by year')
    col1, col2 = st.columns([1,5])
    choose_index = 0
    with col1:
        choose_year = st.selectbox('Judgment year:',
                                   np.sort(years)[:-2])
    with col2:
        cases_option = st.selectbox('Case name:',
                                    year_dir[year_dir['Year'] == choose_year]['Name'])
    choose_case = st.button(f'Go to summary: {cases_option}')
    choose_random = st.button('Select a random case')
    if choose_case:
        choose_index = list(year_dir['Name']).index(cases_option)
        st.write('#')
        st.header(cases_option)
        st.write('##')
        st.subheader("Summary")
        st.write(f'''
             Summary: {data_dictionary_summarised[choose_index]['Background summary']},
             Judgment: {data_dictionary_summarised[choose_index]['Judgment summary']}
             ''' )
    elif choose_random:
        choose_index = np.random.randint(0, len(year_dir))
        random_case = year_dir.at[choose_index, 'Name']
        st.write('#')
        st.header(random_case)
        st.write('##')
        st.subheader("Summary")
        st.write(f'''
             Summary: {data_dictionary_summarised[choose_index]['Background summary']},
             Judgment: {data_dictionary_summarised[choose_index]['Judgment summary']}
             ''' )
    st.write('##')
    st.subheader('Q&A')
    new_q = st.text_input('Question: ', placeholder='Ask a question about this case')
    ask = st.button('Ask')
    if ask:
        question = "What was the outcome?"
        text_type = "summ"
        key = 23
        url = f"https://uksc-question-app-jaefennyiq-ew.a.run.app/question?type={text_type}&key={key}&question={question}"
        response = requests.get(url).json()
        st.write("Question: ", question)
        st.write("Answer: ", response["answer"]["answer"])
        st.write("Confidence: ", str(response["answer"]["score"]))
