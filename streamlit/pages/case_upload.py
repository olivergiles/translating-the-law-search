import streamlit as st
import pandas as pd
import requests

def app():
    st.title('Translate the Law')
    st.write('##')
    st.subheader('Summarise a new case')
    txt = st.text_area('Paste legal text and press enter to get your summary:',
                        max_chars=None,
                        placeholder=None)
    if st.button('Enter'):
        summary = requests.get(f'https://uskc-summarizer-app-jaefennyiq-ew.a.run.app/summary?text="{txt}"').\
            json()['summary']
        st.write('Summary: ', summary[0]["summary_text"])
    else:
        pass

    #sometimes after we've been using the site too much, the multiapp nav gets weird
    #(aka stops working)
