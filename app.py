from email.policy import default
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlalchemy
import os
import yfinance as yf
import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error,mean_absolute_error


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
prediction=None

class Test(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    uname = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"


@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        name=request.form['name']
        uname=request.form['uname']
        password=request.form['password']
        test= Test(name=name,uname=uname,password=password)
        db.session.add(test)
        db.session.commit()
    
    allTest=Test.query.all()
    return render_template('index.html',allTest=allTest)

@app.route("/delete/<int:sno>")
def delete(sno):
    alltest=Test.query.filter_by(sno=sno).first()
    db.session.delete(alltest)
    db.session.commit()   
    print(alltest.sno)
    name=alltest.name
    return "DONE"

@app.route("/login.html",methods=['GET','POST'])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        alltest=Test.query.filter_by(name=name,password=password).first()
        # db.session.delete(alltest)
        db.session.commit()  
        if str(alltest) != 'None':
           print("ok done")
           return render_template('home.html')
        else:
            print("no") 
            return render_template('no.html')  
         
    allTest=Test.query.all()
    return render_template('login.html',allTest=allTest)
  
# ('index.html',allTest=allTest)
@app.route("/home.html",methods=['GET','POST'])
def home():
    if request.method=='POST':
        start_date=request.form['start_date']
        end_date=request.form['end_date']
        currency=request.form['currency']
        days=int(request.form['days'])
        print(start_date)
        print(end_date)
        print(currency)
        print(days)
        df=yf.download(currency,start_date,end_date)
        df=df.dropna()
        print(df.head())
        print(df['Adj Close'])
        # adj_close=df['Adj Close']
        # open=df['Open']
        # print(open)
        model=sm.tsa.arima.ARIMA(df['Adj Close'], order=(4,1,0))
        model_fit=model.fit()
        # index_future_dates=pd.date_range(start='2022-03-11',end='2022-03-15')
        # print(index_future_dates)
        print(len(df))
        print(len(df)+days)
        pred=model_fit.predict(start=len(df), end=len(df)+days, exog=None, dynamic=False)
        # pred.index=index_future_dates
        print(pred)
        # print("done")
    return render_template('result.html',pred=pred)

if __name__ == "__main__":
    app.run(debug=True)
# comment added
