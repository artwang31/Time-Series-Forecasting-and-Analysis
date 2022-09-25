# Time-Series-Forecasting-and-Analysis
Predicted the revenue of vendors via time series forecasting and analysis.

**ALL PERSONAL AND/OR UNIQUE IDENTIFIERS HAVE BEEN REMOVED FROM ALL SAMPLE DATA**

**CONTEXT**

This project required me to forecast the revenue of a given number of clients.

**METHODOLOGY AND PROCESS**

**Preparing the Data for Analysis**  

I began my project by loading the required libraries to perform my analysis, reading in the dataset, and looking at the data types and structures of each column. This step was important because it allowed me to understand the data I am working with and what types of data preprocessing I needed to do before analysis. 

I then cleaned the data for only vendors with a vendor_id of 25 and 31, looked for any negative values that could trigger outliers, and then performed math, item_price * item_cnt_day, to account for total sales for the day. 

As the goal of the project was to forecast the revenue for the remainder of December 2015, I then used the group_by function to aggregate all the total sales for the day, and then organized the aggregations by week for the time series analysis.  

Having cleaned the data, I learned that there were a few weekly outliers in the data for November 2015. The two weeks had no sale items or purchases, this was an aberration to me because the data showed positive sales for November 2013 and 2014. Thus, I removed these outliers as I attributed the lack of information as either a data engineering/storage issue, unreported revenue data, an item inventory issue, or some other unique circumstance as the historical data did not suggest that there should have been no observations for the weeks of November 2015. 

**Conducting Exploratory Data Analysis**

Before I can adequately forecast revenue, I had to check if the data showed any trends, characteristics, or unique findings. Thus, I performed some exploratory data analysis by plotting the data over time.

![Exploratory Data Analysis Visualization](https://github.com/artwang31/Time-Series-Forecasting-and-Analysis/blob/main/1%20EDA%20Plot.png)

Once I did this, the data seemed to reveal some sort of seasonality in weeks 48-50 and weeks 98-102. This could mean that more purchases are made by vendors 25 and 31 towards the later part of the calendar year.

**Checking for Seasonality and Stationarity**

Looking deeper, I created another plot to look at the mean and standard deviations over time. The plot indicated that the data is indeed stationary but it also exhibits seasonality. The mean and standard deviation lines were smoothed with a lag of four weeks to check for any non-stationarity issues.

![Exploratory Data Analysis Visualization](https://github.com/artwang31/Time-Series-Forecasting-and-Analysis/blob/main/2%20EDA%20Mean%20SD.png)

To further test for stationarity issues, I performed an Augmented Dickey-Fuller test to example the test statistic, p- values, and coefficients. I needed to perform this test to make sure that the data are non-stationary (has some time-dependent structure such as an upward or downward trend in the data).

![Exploratory Data Analysis Visualization](https://github.com/artwang31/Time-Series-Forecasting-and-Analysis/blob/main/3%20Dickey%20Fuller.png)

The results indicated a test statistic that was smaller than all the critical values and a p-value that was lower than the .05 level-of-significance threshold. These were all good signs and pointed to the data being stationary, as the more negative the test statistic, the more likely we are to reject the null hypothesis (the data are non-stationary).

Moreover, additional plots were created to compare trend lines, seasonality, and the residual plot, to the original data.

![Exploratory Data Analysis Visualization](https://github.com/artwang31/Time-Series-Forecasting-and-Analysis/blob/main/4%20Multi%20Plots.png)

**Implementing the Forecasting Model**

While the data passed the tests I implemented (smoothed mean visualization and Dickey Fuller test) for stationarity, it did not pass the seasonality test. Therefore, to perform an adequate model forecast, I decided to use the Seasonal Autoregressive Integrated Moving Average model, or SARIMA.

However, before creating the model, I visualized an Auto Correlation Function (ACF) and Partial Auto Correlation Function (PACF) to test the correlations between values separated by the given time period, as doing this provided me the necessary input parameters (p, d, q) for the SARIMA model. By looking at the two plots, there were more significant points out of the 0.02 significant level in the PACF plot and therefore the SARIMA model was the right choice.

![Exploratory Data Analysis Visualization](https://github.com/artwang31/Time-Series-Forecasting-and-Analysis/blob/main/5%20ACF%20PACF.png)

Once I implemented the model, I plotted the actual revenue of the data set in blue along with my forecasted revenue in orange. A side-by-side comparison effectively showcased that the model is effective in forecasting revenue.

![Exploratory Data Analysis Visualization](https://github.com/artwang31/Time-Series-Forecasting-and-Analysis/blob/main/6%20Actual%20Forecast.png)

**Predicting and Forecasting the Data**

Finally, to predict the forecasted revenue for December 2015, I had to extend the date range in my data set and then predict the revenue for these new weeks. Once the timeline was extended, I then predicted the revenue on the new data in relation to the historical data provided to me. The prediction was extended by the orange line seen below and exhibited similar characteristics in terms of seasonality as the historical data. Based on my model,

The total revenue of vendors 25 and 31 for the remainder of December 2015 is approximately $3,071,548.

![Exploratory Data Analysis Visualization](https://github.com/artwang31/Time-Series-Forecasting-and-Analysis/blob/main/7%20Result.png)

**Conclusion and Final Thoughts:**

The data and its nuances provided some challenging issues but revealed some interesting insights. In my analysis, because of the outliers (no data) that occurred in November 2015, this unique circumstance (not represented in previous years, 2013 and 2014) pushed the 2015 calendar year’s seasonal peak back by a few weeks.
Historically, the peak in sales revenue usually occurs during mid-to-late December, in weeks 48-52 in 2013 and weeks 99-103 in 2014. However, because of the aforementioned outlier of 2-3 weeks which occurred in November 2015, it is my belief that this unique event pushed the expected peak in revenue back by a few weeks in my forecasted 2015 model. As such, what we see in the plot above adequately represents this lag; the peak actually occurs in weeks 156-160, which is approximately 2-3 weeks after the historical peak revenue seasons of 2013 and 2014.

Despite these challenges, in order to improve on my model and analysis, I could have looked at the data in a variety of other ways. These ways included:

- Analyzing other vendors and their revenue trends
- Identifying the item_id to assess which, how many, and/or whether all items were missing for these
months. It could be assumed that the outlier that occurred in November 2015 could be an inventory issue,
unreported data mistake, or a data-flow issue from the Tech Data servers.
- Refining my parameters in SARIMA to account for outliers and differences in lag and timing windows.
- Performing more statistical tests to perfect my model so my predictions are more accurate.
- Consulting with fellow data scientists about my methodology, approach, and forecasting.
 

  
