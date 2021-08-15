#!/usr/bin/env python
# coding: utf-8

# In[67]:


from IPython.display import display, HTML
display(HTML(data="""
<style>
    div#notebook-container    { width: 95%; }
    div#menubar-container     { width: 65%; }
    div#maintoolbar-container { width: 99%; }
</style>
"""))


# In[68]:


# Loading packages for analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import seaborn as sns
pd.options.display.float_format = '{:.2f}'.format
sns.set()
from sklearn.metrics import r2_score, median_absolute_error, mean_absolute_error
from sklearn.metrics import median_absolute_error, mean_squared_error, mean_squared_log_error
from scipy.optimize import minimize
import statsmodels.tsa.api as smt
import statsmodels.api as sm
from tqdm import tqdm_notebook
from itertools import product
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
import warnings
warnings.filterwarnings('ignore')


# In[87]:


# Reading in data
data = pd.read_csv('dataset.csv')  
# Checking data types
data.dtypes
# Converting the date column from an object to date
data['date'] = pd.to_datetime(data['date'])


# In[70]:


# Subsetting data to vendors #25 and #31, added some vendors to check if they purchased anything in November
data = data.loc[(data['vendor_id'] == 25) | (data['vendor_id'] == 31)] #| data['vendor_id'] == 17)] 
# Checking to see if correct vendors were subsetted and understanding data more
pd.unique(data['vendor_id']) # only vendors 25 and 31
len(data) # 421,740 observations 
# Understanding the item_cnt_day, maybe some items were retuned as some negative values exist, -1, -2 
pd.unique(data['item_cnt_day']) 
# Checking to see if any negative item_price
(data['item_price'] < 0).any() # no negative prices
# Creating final item_price per item
data['item_total'] = data['item_price'] * data['item_cnt_day'] 


# In[71]:


# Grouping total revenue for the day
data = data[["date", "item_total"]]
data['date'] = pd.to_datetime(data['date']) - pd.to_timedelta(7, unit='d')
data = data.groupby([pd.Grouper(key='date', freq='w-mon')])['item_total'].sum().reset_index().sort_values('date')


# In[72]:


# *** Dropping the outliers of 0 values in November after intial forecast
data = data.drop([150 , 151])


# In[73]:


# Checking final dataset to work with
data.to_csv('data_check_adw.csv', index=False)


# In[74]:


data.tail(10)


# In[75]:


# Preliminary exploratory data analysis (EDA)
plt.figure(figsize=(28, 12))
plt.plot(data.item_total)
#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
#plt.gcf().autofmt_xdate()
plt.title('Vendor 25 and 31')
plt.ylabel('Price')
plt.xlabel('Time')
plt.grid(False)
plt.show()
# NOTES: by examining the plot, there seems to be a bit of autocorrelation towards the end of the year, weeks 48-52 and similarly weeks 100-104.
# this could indicate seasonality, towards the later half of 2015.
# by looking at the plot, stationarity, it looks like the mean could be constant, no significant upward or downward trends in the data.

# Creating another plot to look at the moving mean
def plot_moving_average(series, window, plot_intervals=False, scale=1.96):
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    plt.figure(figsize=(25,10))
    plt.title('Moving average\n window size = {}'.format(window))
    plt.plot(rolling_mean, 'g', label='Rolling mean trend') # mean = green
    plt.plot(rolling_std, 'r', label='Rolling SD trend') # standard deviation = red
    # Plot confidence intervals for smoothed values
    if plot_intervals:
        mae = mean_absolute_error(series[window:], rolling_mean[window:])
        deviation = np.std(series[window:] - rolling_mean[window:])
        lower_bound = rolling_mean - (mae + scale * deviation)
        upper_bound = rolling_mean + (mae + scale * deviation)
        plt.plot(upper_bound, 'r--', label='Upper bound / Lower bound')
        plt.plot(lower_bound, 'r--')
    plt.plot(series[window:], label='Actual values')
    plt.legend(loc='best')
    plt.grid(True)

# Smoothing by weeks window, the mean looks like it is on a downward trajectory towards december 2015
plot_moving_average(data.item_total, 48) # approximately 4 weeks a month, 48. annual
# NOTES: Judging by the eye test, the mean looks relatively stationary. 


# In[76]:


# Utilizing a Augmented Dickey-Fuller test to check for stationarity to determine how strongly a time series is defined by a trend.
from statsmodels.tsa.stattools import adfuller
# H0: The data are non-stationary (has some time-dependent structure). 
# p-value > 0.05: Fail to reject the null hypothesis (H0), the data are non-stationary.
# p-value < 0.05: Reject the null hypothesis (H0), the data are stationary.
result = adfuller(data.item_total, autolag='AIC')
print(f'ADF Statistic: {result[0]}')
#print(f'n_lags: {result[1]}')
print(f'p-value: {result[1]}')
for key, value in result[4].items():
    print('Critial Values:')
    print(f'   {key}, {value}')    
# NOTES: Test statistic. The more negative this statistic, the more likely we are to reject H0. Reject HO, data are stationary.
# p-value < 0.05, we can reject H0, the data are stationary.   


# In[77]:


from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(data.item_total, freq = 24)

trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plotting original data
plt.figure(figsize=(25,10))
plt.subplot(411)
plt.plot(data.item_total, label = 'Original')
plt.legend(loc = 'best')
# Plotting Trend data
plt.subplot(412)
plt.plot(trend, label = 'Trend')
plt.legend(loc = 'best')
# Plotting Seasonal data
plt.subplot(413)
plt.plot(seasonal, label = 'Seasonal')
plt.legend(loc = 'best')
# Plotting Residual data
plt.subplot(414)
plt.plot(residual, label = 'Residual')
plt.legend(loc = 'best')
plt.tight_layout()


# In[78]:


def tsplot(y, lags=None, figsize=(25, 10), syle='bmh'):
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    with plt.style.context(style='bmh'):
        fig = plt.figure(figsize=figsize)
        layout = (2,2)
        ts_ax = plt.subplot2grid(layout, (0,0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1,0))
        pacf_ax = plt.subplot2grid(layout, (1,1))
        
        # Plotting original data and Dickey-Fuller with p-value.
        y.plot(ax=ts_ax)
        p_value = sm.tsa.stattools.adfuller(y)[1]
        ts_ax.set_title('Time Series Analysis Plots\n Dickey-Fuller: p={0:.5f}'.format(p_value))
        
        # Plotting ACF auto-correlation, and PACF partial auto-correlation
        smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
        smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
        plt.tight_layout()
        
tsplot(data.item_total, lags = 52)


# In[79]:


# Modeling our data 
import statsmodels.api as sm 
# ARIMA inputs and SARIMA inputs
model = sm.tsa.statespace.SARIMAX(data['item_total'], order = (1,1,0), seasonal_order = (1,1,1,54)) #17,28,30,54,58
results = model.fit()


# In[80]:


# Plotting the actual item_total and our forecast
data['forecast'] = results.predict(start = 0, end = 153)
data[['item_total','forecast']].plot(figsize=(25, 10))


# In[81]:


# Forecasting revenue for last few weeks of December 2015
from pandas.tseries.offsets import DateOffset
future_data = data.set_index('date') # setting date as our index
future_data = [future_data.index[-1] + DateOffset(weeks=x) for x in range (0,18)]


# In[82]:


# Adding in our new dates
future_data = pd.DataFrame(index = future_data[1:], columns = data.columns)


# In[83]:


# Cleaning up data for plotting
future_data['date'] = future_data.index
future_data.reset_index(inplace = True)
del future_data['index']


# In[84]:


# Adding our forecasted dataframe and original dataframe together
forecast_data = pd.concat([data, future_data],ignore_index=True)


# In[85]:


# Plotting our forecast data.
forecast_data['forecast'] = results.predict(start = 1, end = 168)
forecast_data[['item_total','forecast']].plot(figsize=(25, 10))


# In[86]:


forecast_data.to_csv('forecast_data_adw.csv', index=False)


# In[ ]:





# In[ ]:




