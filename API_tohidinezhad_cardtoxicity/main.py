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
    # Define intercept and coefficients
    # from predict.crr() R function Package 'cmprsk'
    bfitj_array=[0.00332148046796498, 0.00704252318188995, 0.00680807619210244, 0.0031499383078194, 0.00484916989995649, 0.00341262479774758, 0.00494599020759115	,0.00296349943121998	,0.00345366709214391	,0.00362648429291061	,0.00418264710845545	,0.00302764782129292	,0.000887856938295995	,0.00365583200055486	,0.00240905678629641	,0.00500582322280056	,0.0015689443672039	,0.00371440727883678	,0.00278396258514993	,0.00230551534195185	,0.00178567396713869	,0.00187118290948318	,0.000658830383426973	,0.00267463575367071	,0.00208614130013182	,0.00287334782786033	,0.00223723081752879	,0.00383392730297976	,0.00235998328142089	,0.00326304981299299	,0.000864038793188006	,0.00179110720667369	,0.0038011665601519	,0.00202847820989097	,0.00211095773600686	,0.00109268863820134	,0.00233885619214348	,0.00121972074648294	,0.001293411808873	,0.00136664839834629	,0.00146705295510893	,0.00157655765592158	,0.00181300856186351	,0.00185287095288774	,0.0019564565695927	,0.00205558204156154	,0.00231505681797333	,0.00287871156288563]

    LB=0
    for i in input_dict:
        if i=='Age' and input_dict[i]>70:
            LB=LB+0.27927258
        if i=='BMI' and input_dict[i]=='Underweight':
            LB=LB+0.93495631
        if i=='BMI' and input_dict[i]=='Overweight':
            LB=LB+(-0.07729853)
        if i=='BMI' and input_dict[i]=='Obese':
            LB=LB+(-0.1610674)
        if i=='Cardiac diseases' and input_dict[i]=='Yes':
            LB=LB +0.41476678
        if i=='Vascular diseases' and input_dict[i]=='Yes':
            LB=LB +0.31604012
        if i=='Pacemaker/defibrillator' and input_dict[i]=='Yes':
            LB=LB +0.69627766
        if i=='Chemotherapy' and input_dict[i]=='Cisplatin-etoposide':
            LB=LB +0.14794705       
        if i=='Chemotherapy' and input_dict[i]=='Carboplatin-etoposide':
            LB=LB +0.44799406
        if i=='Chemotherapy' and input_dict[i]=='Other':
            LB=LB +(-0.10023631)
        if i=='QRS interval' and input_dict[i]<80:
            LB=LB +(-0.12952556)
        if i=='QRS interval' and input_dict[i]>100:
            LB=LB +0.3148878
        if i=='Heart Volume' and input_dict[i]>=792:
            LB=LB +0.41634732
        if i=='Right lung volume' and input_dict[i]<2161:
            LB=LB +0.35404859
        if i=='Left atrium Dmax' and input_dict[i]>=63:
            LB=LB +0.49512383
        if i=='Esophagus' and input_dict[i]>=1:
            LB=LB +0.39459581
        if i=='Left lung Dmax' and input_dict[i]<6:
            LB=LB +0.6001245
             
    prob=1-math.exp(-np.sum(np.multiply(bfitj_array,math.exp(LB))))
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