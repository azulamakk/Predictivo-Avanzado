import streamlit as st
from PIL import Image

#Insert a picture
# First, read it with PIL
st.text('Imagen')
image = Image.open('chuck.jpg')
# Load Image in the App
st.image(image)


import seaborn as sns
import numpy as np
import pandas as pd

# Load the Dataset
df = sns.load_dataset('tips')

# Add Lat Long
latlong = {'NY': {'lat': 40.730610, 'lon': -73.935242},
           'London': {'lat': 51.509865,'lon': -0.118092},
           'Paris': {'lat': 48.864716, 'lon':2.349014},
           'Sao Paulo': {'lat': -23.533773,'lon': -46.625290},
           'Rome': {'lat': 41.902782,'lon': 12.496366}
           }

city = ['Paris', 'London', 'NY', 'Sao Paulo', 'Rome']
city_random = np.random.choice(city, 244)

# Add Cols
df['city'] = city_random
df['lat'] = [latlong[city]['lat'] for city in city_random]
df['lon'] = [latlong[city]['lon'] for city in city_random]

# Map
st.text("")
st.text('Mapa')
map_df = df[['lat', 'lon']]
st.map(map_df, zoom=1)

st.text("")
st.text('Radio Button')
st.radio('Choose your option', options=('Option 1', 'Option 2', 'Option 3'))
         
# Slider
st.text("")
st.text('Slider')
st.slider('<-- Slide to the sides -->', min_value=0, max_value=10, value=5, step=1)

# Multiselect
st.text("")
st.text('Multiselect')
st.multiselect('What are your favorite colors',
            ['Green', 'Yellow', 'Red', 'Blue'],
            ['Blue', 'Green']) #pre-selected

# Selectbox
st.text("")
st.text('Select box')
st.selectbox('Select Box',options=('Option 1', 'Option 2', 'Option 3'))

# text input
st.text("")
st.text('Text input')
title = st.text_input('My App Text Input', 'Write Something...')
st.write('You wrote:  ', title)

# Adding a text in the sidebar
st.sidebar.text('Ejemplo de sidebar')
# Add a radio button
st.sidebar.radio('label', options=[])