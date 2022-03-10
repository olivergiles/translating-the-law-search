import streamlit as st
import pandas as pd
import requests

questions_df = pd.DataFrame({'questions': ['Please select', 'Sample Question 1', 'Sample Question 2']})

def app():
    st.title('Translate the Law: Question API Example')
    st.write('#')
    ### Example for connection to question answering api
    question = "what was the outcome?"
    text_type = "summ" #full
    key = 0
    url = f"https://uksc-question-app-jaefennyiq-ew.a.run.app/question?type={text_type}&key={key}&question={question}"
    response = requests.get(url).json()
    st.write("Question answer: ", response["answer"]["answer"])
    st.write("###")
    st.write("Confidence: ", str(response["answer"]["score"]))
    ### End of example
    # st.subheader('Search for a case by keyword')
    # st.caption("Need to quickly understand a UK Supreme Court case?\
    #     Search the one you're looking for by name, justice, case ID, or other keyword.")
    # query = st.text_input('Search for case by keyword',
    #               placeholder='Enter case detail or topic')
    # if st.button('Enter'):
    #     st.write('Search results for: ', query)
    # else:
    #     pass
    # if st.button('casenameplaceholder'):
    #     st.write('#')
    #     st.header('casenameplaceholder')
    #     st.write('##')
    #     st.subheader("Summary")
    #     st.write("The model-generated summary will show up here,\
    #         along with some of the other relevant case details such as case id number,\
    #         judgment date, names of justices, and neutral citation number(?)")
    #     st.write('##')
    #     st.subheader('Q&A')
    #     col1, col2 = st.columns([2,3])
    #     with col1:
    #         our_q = st.selectbox('Suggested questions', questions_df['questions'])
    #     with col2:
    #         new_q = st.text_input('Or write your own', placeholder='Ask a question about this case')
    #     if our_q != 'Please select':
    #         st.write(f'Q: {our_q}')
    #     else:
    #         st.write(f'Q: {new_q}')
    #     if new_q:
    #         answer = requests.get(f'https://uskc-summarizer-app-jaefennyiq-ew.a.run.app/')
    #         st.write(new_q, answer)