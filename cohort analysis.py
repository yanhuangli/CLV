import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df_order = pd.read_csv('orders.txt',parse_dates=['orderdate'],sep='\t',encoding='ISO-8859-1')
df_customer = pd.read_csv('customer.txt',sep='\t',encoding='ISO-8859-1')
df_order = df_order[['orderid','customerid','orderdate','totalprice']]
df = df_order.merge(df_customer[['customerid','householdid']],left_on='customerid',right_on='customerid')



#order month =every transaction time,whereas cohort = the first month of the householdid

import datetime as dt
df['one_month'] = df['orderdate'].apply(lambda x: dt.datetime(x.year,x.month,1))
df1 = df.groupby('householdid').agg({'one_month':lambda x:min(x)}).reset_index()
df1.columns = ['householdid','cohort']
df = df.merge(df1,left_on='householdid',right_on='householdid')s
df['cohort_month'] = df.orderdate.apply(lambda x : x.year*12+x.month)-\
                     df.cohort.apply(lambda x:x.year*12+x.month)+1
df['cohort'] = df['cohort'].dt.strftime('%Y/%m')
df2 = df.groupby(['cohort','cohort_month'])['householdid'].nunique().reset_index()

#calculate retention rate

df2 = df2.pivot(index = 'cohort',values = 'householdid',columns = 'cohort_month')

df_retention = df2.divide(df2.iloc[:,0],axis = 0).round(3)*100


import seaborn as sns

sns.heatmap(df_retention)
plt.figure(figsize=(18,18))
plt.show()
