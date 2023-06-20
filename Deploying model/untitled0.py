# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 22:49:52 2023

@author: Chamberlain
"""


import numpy as np
import pickle
import streamlit as st


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data










load_model=pickle.load(open('C:/Users/Chamberlain/Desktop/Deploying model/trained_model.sav', 'rb'))

# creating fuctions for crop prediction
# on stremlit fuctions or methods are used to build the interactive environment on the web app


def crop_prediction(input_crop_data):
    
    input_numpy_array=np.array(input_crop_data)
    input_reshaped= input_numpy_array.reshape(1,-1)

    pred=load_model.predict(input_reshaped)
    pred.item().title()
    return pred.item().title()

   
def main():
    st.title('Crop Yield Prediction Web Application')
    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)
  
    if choice == "Home":
        st.subheader("This is web application uses Feed-Foward neural network to predict the suitable crop that can be grown baed on soil and atmospheric feature.")
        
    elif choice == "Login":
        st.subheader("Login to your Account")
        
        username = st.text_input("User Name")
        password = st.text_input("Password",type='password')
        if st.button("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
           
        
						
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
            else:
                st.warning("Incorrect Username/Password")
                
    
    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')
        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")
		
		
		

	

    
    
if __name__=='__main__':
    main()
