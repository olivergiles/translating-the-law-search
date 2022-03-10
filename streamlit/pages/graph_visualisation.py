import streamlit as st
import pandas as pd
import plotly.express as px


clustering_data = st.cache(pd.read_csv('graph_viz.csv'))

def app():
    button = st.button('Launch cluster')
    if button:
        fig = px.scatter_3d(clustering_data, x='x', y='y', z='z',color = clustering_data['labels'])
        st.plotly_chart(fig)
