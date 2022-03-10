import streamlit as st
from multiapp import MultiApp
from pages import case_search, case_upload, year_select
import os
import sys
import urllib.parse
import streamlit as st
from elasticsearch import Elasticsearch
import json
import utils, templates, search
from functions.get_search_data import get_search_data
import streamlit as st
import pandas as pd
import plotly.express as px





class vis_app:
    def app():
        base_path = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(base_path, "graph_viz.csv")
        clustering_data = pd.read_csv(csv_path)
        button = st.button('Launch cluster')
        if button:
            fig = px.scatter_3d(clustering_data, x='x', y='y', z='z',color = clustering_data['labels'])
            st.plotly_chart(fig)

INDEX = 'uksc_data'
PAGE_SIZE = 5
DOMAIN = 'es'
PORT = 9200
es = Elasticsearch(host=DOMAIN)
utils.check_and_create_index(es, INDEX)

os.environ['INDEX'] = INDEX
os.environ['PAGE_SIZE'] = str(PAGE_SIZE)
os.environ['DOMAIN'] = DOMAIN
index = os.environ['INDEX']

@st.experimental_memo
def get_cases():
    return get_search_data()

cases = get_cases()

try:
    if os.environ['RUN'] == 'done':
        pass
except:
    utils.index_cases(es, index, cases, False)
    os.environ['RUN'] = 'done'

app = MultiApp()

app.add_app('Select case from year', year_select.app)
app.add_app('Search for a case by keyword', search.app)
app.add_app('Upload your own text', case_upload.app)
app.add_app('Clustering', vis_app.app)
#app.add_app('Question API Example', case_search.app)

app.run()
