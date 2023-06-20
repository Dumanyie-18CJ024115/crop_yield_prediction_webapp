## -*- coding: utf-8 -*-
"""
#Created on Sun Apr 30 11:36:54 2023

#@author: Chamberlain
#"""

import streamlit as st
from sklearn import datasets
import streamlit_authenticator as stauth
hashed_passwords = stauth.Hasher(['abc123', 'ddc123']).generate()

import yaml
from yaml.loader import SafeLoader

with open('C:/Users/Chamberlain/Desktop/Deploying model/loggin.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
    
name, authentication_status, username = authenticator.login('Login', 'main')
 
    
if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'sidebar', key='unique_key')
    if username == 'admin' :
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
    elif username == 'dchamberlain':
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')
        
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    
if st.button("Reset",):
    try:
        if authenticator.reset_password(username, 'Reset password','sidebar'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)
elif st.sidebar("Register"):
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)
    
