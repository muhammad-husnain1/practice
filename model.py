# import yfinance as yf
# import pandas as pd
# import numpy as np
# import math
# import statsmodels.api as sm
# from statsmodels.tsa.stattools import adfuller
# from statsmodels.tsa.arima_model import ARIMA
# from statsmodels.tsa.ar_model import AutoReg
# from sklearn.metrics import mean_squared_error,mean_absolute_error

# df=yf.download('BTC-USD')
# df=df.dropna()
# print('shape of data',df.shape)
# df
# from pmdarima import auto_arima
# stepwise_fit = auto_arima(df['Adj Close'], trace=True,
# suppress_warnings=True)