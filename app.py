import streamlit as st
from itertools import combinations

st.title("Dinner Party Seating Optimiser")
st.write("Welcome! This app will help you seat your guests for maximum happiness!")
st.write("Lets get started!")

names=[]
for i in range(6):
    name = st.text_input(f"Guest {i+1}", 
                         placeholder="eg. Keith")
    names.append(name)

st.write(names)

if all(names):
    pairs = list(combinations(names, 2))

    happiness_dict = {}

    for pair in pairs:
        st.write(f"What is the happiness of {pair[0]} and" 
                f" {pair[1]} sitting next to eachother?"
        )
        happiness = st.slider(f"{pair}'s happiness score", 
                            min_value=1, max_value=10, 
                            value=5)
        happiness_dict[pair] = happiness

