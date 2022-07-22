from tkinter.font import names
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(page_title='Cars Dashboard',page_icon=':bar_chart:',layout='wide')

data = pd.read_csv('Automobile_data.csv')
data = data.drop(labels=['symboling', 'normalized-losses','engine-type'],axis=1)
data = data.dropna(axis = 0, how ='any')

data_filtered = data
st.sidebar.header('Apply Filters')

if st.sidebar.checkbox('Enable'):

    make = st.sidebar.multiselect('Make:',options=data['make'].unique(),default=data['make'].unique())
    data_filtered = data_filtered[data['make'].isin(make)]

    fuel = st.sidebar.radio('Fuel Type:',options=data['fuel-type'].unique())
    data_filtered = data_filtered[data['fuel-type']==fuel]

    aspiration = st.sidebar.multiselect('Aspiration Type:',options=data['aspiration'].unique(),default=data['aspiration'].unique())
    data_filtered = data_filtered[data['aspiration'].isin(aspiration)]

    doors = st.sidebar.select_slider('Number of Doors:',options = data['num-of-doors'].unique())
    data_filtered = data_filtered[data['num-of-doors']==(doors)]

    body_style = st.sidebar.radio('Body Style:',options=data['body-style'].unique())
    data_filtered = data_filtered[data['body-style']==(body_style)]

    cylinder = st.sidebar.select_slider('Number of Cylinders:',options=sorted(data['num-of-cylinders'].unique()))
    data_filtered = data_filtered[data['num-of-cylinders']==(cylinder)]

    engine_size = st.sidebar.slider('Engine Size:',min_value=int(data['engine-size'].min()),max_value=int(data['engine-size'].max()),value=int(data['engine-size'].max()))
    data_filtered = data_filtered[data['engine-size']<=(engine_size)]

    price = st.sidebar.slider('Price:',value=(int(data['price'].min()),int(data['price'].max())))
    data_filtered = data_filtered[data['price']>=price[0]]
    data_filtered = data_filtered[data['price']<=price[1]]

    if st.sidebar.button('Reset'):
        data_filtered = data

st.title('Car Details Dashboard')
st.markdown('##')
st.dataframe(data_filtered[['make','fuel-type','num-of-doors','body-style','price']])
if st.checkbox('More Details'):
    st.dataframe(data_filtered)
st.markdown('---')

fig = make_subplots(rows=1, cols=2)

fuel_type_bar = data_filtered.groupby(['fuel-type']).count().reset_index()
fuel_types = px.bar(fuel_type_bar,y=data_filtered.groupby(['fuel-type']).size(),x='fuel-type',orientation='v',title='Fuel Type',width=625)
#fuel_types.update_layout(plot_bgcolor='rgba(0,0,0,0)',yaxis=(dict(showgrid=False)))

st.plotly_chart(fuel_types)

body_type_bar = data_filtered.groupby(['body-style']).count().reset_index()
body_types = px.pie(body_type_bar,values=data_filtered.groupby(['body-style']).size(),names='body-style',title='Body Style',width=625)
#body_types.update_layout(plot_bgcolor='rgba(0,0,0,0)',yaxis=(dict(showgrid=False)))

st.plotly_chart(body_types)

price_per_brand = px.box(data_filtered,y='price',x='make',orientation='v',title='Prices per Brands',width=1250)
price_per_brand.update_layout(plot_bgcolor='rgba(0,0,0,0)',xaxis=(dict(showgrid=False)),yaxis=(dict(showgrid=False)))

st.plotly_chart(price_per_brand)