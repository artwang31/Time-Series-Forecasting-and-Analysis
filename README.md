# Time-Series-Forecasting-and-Analysis
Predicted the revenue of vendors via time seeries forecasting.  

**ALL PERSONAL AND/OR UNIQUE IDENTIFIERS HAVE BEEN REMOVED FROM ALL SAMPLE DATA**  


**CONTEXT**
This project required me to forecast the revenue of a given number of clients. 

**METHODOLOGY AND PROCESS**

**Preparing the Data for Analysis**
I began my project by loading the required libraries to perform my analysis, reading in the dataset, and looking at the data types and structures of each column. This step was important because it allowed me to understand the data I am working with and what types of data preprocessing I needed to do before analysis. 

I then cleaned the data for only vendors with a vendor_id of 25 and 31, looked for any negative values that could trigger outliers, and then performed math, item_price * item_cnt_day, to account for total sales for the day. 

As the goal of the project was to forecast the revenue for the remainder of December 2015, I then used the group_by function to aggregate all the total sales for the day, and then organized the aggregations by week for the time series analysis.  

Having cleaned the data, I learned that there were a few weekly outliers in the data for November 2015. The two weeks had no sale items or purchases, this was an aberration to me because the data showed positive sales for November 2013 and 2014. Thus, I removed these outliers as I attributed the lack of information as either a data engineering/storage issue, unreported revenue data, an item inventory issue, or some other unique circumstance as the historical data did not suggest that there should have been no observations for the weeks of November 2015. 





