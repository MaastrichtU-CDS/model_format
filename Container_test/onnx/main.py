#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 16:40:35 2024

@author: p70091732
"""
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import math
#import numpy as np
import json
import onnxruntime as ort

app=Flask(__name__)
CORS(app)
api=Api(app)

def prob(input_dict):
    model_name="willemsen_tubefeed.onnx"
    ort_sess = ort.InferenceSession(model_name, providers=['AzureExecutionProvider', 'CPUExecutionProvider'])
    
    input_array=list(input_dict.values())
    outputs = ort_sess.run(None, {'input': [input_array]})      
    #[19.5,-8,1,0,1,1,1,0,36,29]  
    # input_dict={"BMI":19.5, "WeightLoss":-8, "TF":1, "PS":0, 
    #             "Tumorlocation":1, "Tclassification":1,
    #             "Nclassification":1, "Systherapy":0,
    #             "RTdose_subman":36, "RTdosesalivary":29}
    
    
    return outputs


@app.route("/predict",methods=["POST"])
def predict():
    #data=request.get_json()
    # with open('input.json', 'r') as openfile:
    #     # Reading from json file
    #     inputdata = json.load(openfile)
    inputdata=request.get_json()
    
    predicted = prob(inputdata)
    return jsonify({"Prediction":predicted[1][0][1]})

if __name__ == "__main__":
    app.run(debug=True)