import streamlit as st 
import pandas as pd 
import time as ts 
from datetime import time 
# to remove the humburger and footer 
st.markdown("""
            <style>
            .st-emotion-cache-w3nhqi.ef3psqc5
            {
                visibility: hidden;
            }
            .st-emotion-cache-1huvf7z.ef3psqc6
            {
                visibility: hidden
            }
            </style>
            """,unsafe_allow_html=True)

st.title("Timer app with progress ")
st.markdown("---")

def ConvertToSec(value):
    m,s,ms = value.split(":")
    t_s = int(m)*60 + int(s) + int(ms)/1000
    return t_s

val = st.time_input("Set Timer" , value = time(0,0,0))
if str(val) == "00:00:00":
    st.write("Please set timer")
else:
    sec = ConvertToSec(str(val))
    bar = st.progress(0)
    per = sec/100 
    progress_status = st.empty()
    for i in range(100):
        bar.progress(i+1)
        progress_status.write(str(i+1) +" % ")
        ts.sleep(per)
st.write ("Timer is over ")