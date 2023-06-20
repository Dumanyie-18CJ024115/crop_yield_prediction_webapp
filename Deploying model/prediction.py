# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
## run the code to test the model.
import numpy as np
import pickle


load_model=pickle.load(open('C:/Users/Chamberlain/Desktop/Deploying model/trained_model.sav', 'rb'))


input_crop_data= (85,58,41,21.77046169,80.31964408,7.038096361,226.6555374)
input_numpy_array=np.array(input_crop_data)
input_reshaped= input_numpy_array.reshape(1,-1)

pred=load_model.predict(input_reshaped)
pred.item().title()
print('The predicted crop to grow here is:',pred.item().title())

