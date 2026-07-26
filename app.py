import streamlit as st
from itertools import combinations, permutations
from pulp import *
import html

st.title("Dinner Party Seating Optimiser")
st.write("Welcome! This app will help you seat your guests for maximum happiness!")
st.write("Lets get started!")

def seat_box(name, colour):
        safe_name = html.escape(name)
        return f'<div style="background-color:{colour}; \
        padding:15px; text-align:center; color:black; \
        border-radius:6px; font-weight:bold; min-height:70px\
        ">{safe_name}</div>'

#user inputs names
names=[]
for i in range(6):
    name = st.text_input(f"Guest {i+1}", 
                         placeholder="eg. Keith", 
                         max_chars= 30)
    names.append(name)


#user ranks the happiness of each pair
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

    #optimisation occurs
    if st.button("Optimise Seating!"):

        model= LpProblem('Dinner_party_seating_optimiser', LpMaximize)

        #variable feeds
        adjacent_pairs = {(0,1) : 1, (1,2): 2, (2,3):1, (3,4):1, 
                        (4,5):2, (5,0):1}
        perm_names = list(permutations(names,2))

        #decision variables
        x = LpVariable.dicts("seat", [(g,s,) for g in names for s 
                                    in range(6)], cat='Binary')
        z = LpVariable.dicts("pair", [(g1,g2,s1,s2) for (g1,g2) in 
                                    perm_names for (s1,s2) in
                                    adjacent_pairs], 
                                    cat='Binary')

        #obj function
        model += (lpSum(happiness_dict[g1,g2]*adjacent_pairs[s1,s2]
                        *(z[(g1,g2,s1,s2)] + z[(g2,g1,s1,s2)]) for 
                        (g1,g2) in pairs for (s1,s2) in 
                        adjacent_pairs))

        #constraints
        #1. each guest is seated once
        for s in range(6):
            model += lpSum(x[(g,s)] for g in names) == 1

        #2. each seat is used once
        for g in names:
            model += lpSum(x[(g,s)] for s in range(6)) == 1

        #3. to linearise z to be binary
        for (s1,s2) in adjacent_pairs:
            for (g1,g2) in perm_names:
                model += z[(g1,g2,s1,s2)] <= x[(g1,s1)]
                model += z[(g1,g2,s1,s2)] <= x[(g2,s2)]
                model += z[(g1,g2,s1,s2)] >= (x[(g1,s1)] 
                                            + x[(g2,s2)] -1)

        #solve model
        model.solve()
        guest_seating_dict = {}

        for s in range(6):
            for g in names:
                if x[g,s].varValue == 1:
                    guest_seating_dict[s] = g


        #seating is shown
        #row1
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown(seat_box(guest_seating_dict[0], 
                                 "#8a2c6c40"), 
                                 unsafe_allow_html=True)

        #row2
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(seat_box(guest_seating_dict[5], 
                         "#A83FA840"), 
                         unsafe_allow_html=True)
        with col2:
            st.markdown(seat_box("","#8B4513"), 
                         unsafe_allow_html=True)
        with col3:
            st.markdown(seat_box(guest_seating_dict[1], 
                         "#A83FA840"), 
                         unsafe_allow_html=True)

        #row3
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(seat_box(guest_seating_dict[4], 
                         "#A83FA840"), 
                         unsafe_allow_html=True)
        with col2:
                    st.markdown(seat_box("", "#8B4513"), 
                                 unsafe_allow_html=True)
        with col3:
            st.markdown(seat_box(guest_seating_dict[2], 
                         "#A83FA840"), 
                         unsafe_allow_html=True)
        #row 4
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown(seat_box(guest_seating_dict[3], 
                         "#8a2c6c40"), 
                         unsafe_allow_html=True)