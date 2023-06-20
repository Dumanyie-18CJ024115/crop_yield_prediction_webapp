# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 22:49:52 2023

@author: Chamberlain
"""


import numpy as np
import pickle
import streamlit as st
import hashlib
import sqlite3
import base64

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user information
c.execute('''CREATE TABLE IF NOT EXISTS users (username text, password text)''')






load_model=pickle.load(open('C:/Users/Chamberlain/Desktop/Deploying model/trained_model.sav', 'rb'))

# creating fuctions for crop prediction
# on stremlit fuctions or methods are used to build the interactive environment on the web app

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local("C:/Users/Chamberlain/Desktop/Deploying model/essentalcrop.jpg")
 

def about():
    st.subheader("About the Final Year Project")
    st.write("This is a web application created by Dumanyie Chamberlain that utilizes a Feed-Forward neural network to predict the appropriate crop that can be grown based on soil and atmospheric features.")

def crop_prediction(input_crop_data):
    
    input_numpy_array=np.array(input_crop_data)
    input_reshaped= input_numpy_array.reshape(1,-1)

    pred=load_model.predict(input_reshaped)
    pred.item().title()
    return pred.item().title()

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def signup():
    st.subheader("Create a new account")
    username = st.text_input("Enter a username")
    password = st.text_input("Enter a password", type="password")
    confirm_password = st.text_input("Confirm your password", type="password")
    
    
    signup_button = st.button("SignUp")
    st.info("Login if you already have account")
    
    if signup_button:
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        st.success("You have successfully created an account. Go to login page")

def login():
    st.subheader("Login to your account")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    login_button = st.button("Login")
    
    if login_button:
        hashed_password = hash_password(password)
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = c.fetchone()
        if user:
            st.success("You have successfully logged in")
            main()
            
            session_id = user[0] # Use the username as the session ID
            st.session_state['session_id'] = session_id
        
            st.experimental_rerun()
        else:
            st.error("Incorrect username or password")


   
def main():
    

    st.title('Crop Yield Prediction Web Application')
    st.subheader("Find the suitable crop to grow on your farm🌳")
    
    N = st.number_input('Enter Nitrogen ratio in the soil', min_value=(0),max_value=(400))
    if N>200:
        st.warning("Nitrogen amount is too high, Nitrogen at this level can delay fruit maturity, add mulch to reduce nitrogen level")
    elif N<0:
        st.warning("Cannot accept negative amount, enter valid value")
        
    P = st.number_input('Enter Phosphorus ratio in the soil', min_value=(0), max_value=(400))
    if P>200:
        st.warning("Phosphorus amount is too high, Phosphorus at this level can staunt plant growth, treat soil with zinc and iron")
    elif P<0:
        st.warning("Cannot accept negative amount, enter valid value")


    K = st.number_input('Enter Potassium ratio in the soil', min_value=(0),max_value=(400) )
    if K>200:
        st.warning("Potassium amount is too high, Potassium at this level can clog soil pores, dissolve excess the excess potassium with water")
    elif K<0:
        st.warning("Cannot accept negative amount, enter valid value")

    
    temperature = st.number_input('Enter Temperature in degree celcius (°C)', min_value=0.0,max_value=100.0, format="%4.1f")
    if temperature>50:
        st.warning("Temperature is too high, soil dwelling organisms cannot survive at this temperature")
    elif temperature<0:
        st.warning("Cannot accept negative amount, enter valid value")

    humidity = st.number_input('Enter humidity measure in percent (%)', min_value=0.000, max_value=100.0, format="%4.1f")
    if humidity>95:
        st.warning("Humidity is too high, Promotes excess bracteria growth which cause root rot")
    elif humidity<0:
        st.warning("Cannot accept negative amount, enter valid value")

    ph = st.number_input('Enter pH value of the soil', min_value=(0.00), max_value=(14.00))
    if ph>10:
        st.warning("Soil pH is too high, Soil fertility can be affected, limiting crop yield")
    elif ph<0:
        st.warning("Cannot accept negative amount, enter valid value")

    rainfall = st.number_input('Enter amount of Rainfall in mm',min_value=0.0,max_value=400.0 , format="%4.1f")
    if rainfall>500:
        st.warning("Rainfall amount is too high, Can leach the nutreints from the soil")
    elif rainfall<0:
        st.warning("Cannot accept negative amount, enter valid value")
    
    #code for prediction
    
    
    
    final_crop_prediction=''
    
    #creating buttons for prediction
    
    if st.button ('Crop Yield Prediction Result'):
        final_crop_prediction= crop_prediction([N, P, K, temperature, humidity, ph, rainfall])
        
    st.success(final_crop_prediction)
    
def logout():
    st.session_state.pop('session_id', None)
    st.info("You have been logged out") 
    st.experimental_rerun() 

menu1 = ["Signup","Login","About"]
menu2 = [ "Predict Crop","Logout"]
menu3 = ["About"]
if 'session_id' not in st.session_state:
    choice = st.sidebar.selectbox("Select an option", menu1)
else:
    choice = st.sidebar.selectbox("Select an option", menu2)



if choice == "Login":
    login()
elif choice == "Signup":
    signup()
elif choice == "Logout":
    logout()
elif choice== "Predict Crop":
    main()
elif choice == "About":
    about()


    
    
    

