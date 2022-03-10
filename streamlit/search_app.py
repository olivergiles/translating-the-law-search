import os
import sys
import urllib.parse
import streamlit as st
from elasticsearch import Elasticsearch
import json
import utils, templates, search
from functions.get_search_data import get_search_data

INDEX = 'uksc_data'
PAGE_SIZE = 5
DOMAIN = 'es'
PORT = 9200
es = Elasticsearch(host=DOMAIN)
utils.check_and_create_index(es, INDEX)

os.environ['INDEX'] = INDEX
os.environ['PAGE_SIZE'] = str(PAGE_SIZE)
os.environ['DOMAIN'] = DOMAIN

def set_session_state():
    """ """
    # default values
    if 'search' not in st.session_state:
        st.session_state.search = None
    if 'tags' not in st.session_state:
        st.session_state.tags = None
    if 'page' not in st.session_state:
        st.session_state.page = 1

    # get parameters in url
    para = st.experimental_get_query_params()
    if 'search' in para:
        st.experimental_set_query_params()
        st.session_state.search = urllib.parse.unquote(para['search'][0])
    if 'tags' in para:
        st.experimental_set_query_params()
        st.session_state.tags = para['tags'][0]
    if 'page' in para:
        st.experimental_set_query_params()
        st.session_state.page = int(para['page'][0])


def main(test):
    st.set_page_config(page_title='Supreme court cases')
    set_session_state()
    st.write(templates.load_css(), unsafe_allow_html=True)
    if test:
        with open("/data/search.json", 'r') as myfile:
            file=myfile.read()
        obj = json.loads(file)
        cases = eval(obj)
    else:
        cases = get_search_data()
    index = os.environ['INDEX']
    utils.index_cases(es, index, cases, test)
    search.app()

if __name__ == '__main__':
    main(False)