#!/usr/bin/env python
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import keras
import tensorflow as tf
from keras.models import model_from_json
import cv2
import json
import numpy as np
import os
import base64
import urllib

loaded = False
app = Flask(__name__)
api = Api(app)

class CatOrDogApi(Resource):
   
    def __init__(self):
        global loaded
        global loaded_model
        print("run init")
        if loaded == False:
            print("--> Start - Loading Model")
            model_root = 'model'
            model_file_json = os.path.join(model_root, 'model.json')
            model_file_h5 = os.path.join(model_root, 'model.h5')

            json_file = open(model_file_json, 'r') 
            loaded_model_json = json_file.read()
            json_file.close()

            loaded_model = model_from_json(loaded_model_json)
            loaded_model.load_weights(model_file_h5)  
            loaded = True
            print("--> End - Loading Model")     
    
    def get(self):
        global loaded_model
        try:
            url = request.get_json()['url']
            urllib.request.urlretrieve(url, filename="tmp.jpg")

            image_data = cv2.imread("tmp.jpg", cv2.IMREAD_GRAYSCALE)
            image_data = cv2.resize(image_data,(96,96))
            image_data = image_data/255

            data1=[]
            data1.append(image_data)
            data1 = np.array(data1)
            data1 = data1.reshape((data1.shape)[0],(data1.shape)[1],(data1.shape)[2],1)    

            predicted_labels = loaded_model.predict(data1)

            labels=['dog' if value>0.5 else 'cat' for value in predicted_labels]

            os.remove("tmp.jpg")

            return json.dumps(labels)
        except AssertionError as error:
            print(error)  

    def post(self):
        global loaded_model
        try:
            url = request.get_json()['url']
            urllib.request.urlretrieve(url, filename="tmp.jpg")

            image_data = cv2.imread("tmp.jpg", cv2.IMREAD_GRAYSCALE)
            image_data = cv2.resize(image_data,(128,128))
            image_data = image_data/255

            data1=[]
            data1.append(image_data)
            data1 = np.array(data1)
            data1 = data1.reshape((data1.shape)[0],(data1.shape)[1],(data1.shape)[2],1)    

            predicted_labels = loaded_model.predict(data1)

            labels=['dog' if value>0.5 else 'cat' for value in predicted_labels]

            os.remove("tmp.jpg")

            return json.dumps(labels)
        except AssertionError as error:
            print(error)  

api.add_resource(CatOrDogApi, '/')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
