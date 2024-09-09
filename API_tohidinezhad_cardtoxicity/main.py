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
import numpy as np
import json

app=Flask(__name__)
CORS(app)
api=Api(app)

def prob_card_tox(input_dict):

    LB=-6.84041
    for i in input_dict:
        if i=='Age at RT':
            LB=LB+0.03928*input_dict[i]
        if i=='BMI' and input_dict[i]=='Underweight':
            LB=LB+0.31514
        if i=='BMI' and input_dict[i]=='Overweight':
            LB=LB+0.58264
        if i=='BMI' and input_dict[i]=='Obese':
            LB=LB+0.58264
        if i=='Alcohol' and input_dict[i]=='Current':
            LB=LB+1.39926
        if i=='Alcohol' and input_dict[i]=='Former':
            LB=LB+(-0.52853)
        if i=='Cardiac procedures' and input_dict[i]=='Yes':
            LB=LB +0.84555
        if i=='Tumor location' and input_dict[i]=='Lower':
            LB=LB +0       
        if i=='Tumor location' and input_dict[i]=='Upper':
            LB=LB +0.94432 
        if i=='Tumor location' and input_dict[i]=='Middle':
            LB=LB +(-1.58108) 
        if i=='Tumor location' and input_dict[i]=='Mediastinum or hilum':
            LB=LB +0.7346  
        if i=='FEV1 (%)':
            LB=LB + (-0.01084)*input_dict[i]
        if i=='Creatinine (μmol/L)':
            LB=LB + 0.00817*input_dict[i]
        if i=='Chemotherapy' and input_dict[i]=='Sequential':
            LB=LB +0       
        if i=='Chemotherapy' and input_dict[i]=='Concurrent':
            LB=LB +1.18358
        if i=='Chemotherapy' and input_dict[i]=='None':
            LB=LB +0.12609
        if i=='Left atrium Dmax':
            LB=LB +0.02173*input_dict[i]
    
    prob=1/(1+math.exp(-LB))         
    return prob


class prediction(Resource):
    def get(self,inputdata):
        inputdata=request.args.get('input')
        print(input)
        prediction=prob_card_tox(inputdata)
        return str(prediction,".3f")
    
class getData(Resource):
    def get(self):
        with open('input.json', 'r') as openfile:

            # Reading from json file
            res = json.load(openfile)
        return res

api.add_resource(prediction, "/prediction/<int:inputdata>")
api.add_resource(getData, "/api")

@app.route("/predict",methods=["POST"])
def predict():
    #data=request.get_json()
    with open('input.json', 'r') as openfile:
        # Reading from json file
        inputdata = json.load(openfile)
    predicted = prob_card_tox(inputdata)
    return jsonify({"Prediction":predicted})

if __name__ == "__main__":
    app.run(debug=True)