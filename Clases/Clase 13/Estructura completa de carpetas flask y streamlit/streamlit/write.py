import seaborn as sns
import pandas as pd
import streamlit as st

# Load Dataset
df = sns.load_dataset('tips')

# # Page Title
st.title('Examples of what st.write() can do')

# Text + emoji
st.write('Hello :sunglasses: :heart: ')

# Calculations
st.write(1+1)

# Variables
a = 2**2
st.write(a)

# Table
st.write(df.head(2))

# Multiple
st.write('st.write("text", df)', df.head(3))