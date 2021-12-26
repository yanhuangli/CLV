import pandas as pd
import numpy as np

df=pd.read_csv('orders.txt',sep='\t',encoding='ISO-8859-1',parse_dates=['orderdate'])
# print(df.head())
# print(df.columns)
# print((df.dtypes))
#LTV = AOV*MARGIN*FREQ/CHURN - ACT

margin = 0.5
ac = 1
customer = df.groupby('customerid').agg({'orderdate':lambda x:(x.max()-x.min()).days,
                                        'totalprice':lambda x:sum(x),
                                         'orderid':lambda x:len(x)})


customer = customer[customer['orderdate']>0]
retention = customer[customer['orderid']>1].shape[0]/customer.shape[0]
avg_order = customer['totalprice'].sum()/customer['orderid'].sum()
freq = customer['orderid'].sum()/customer['orderdate'].sum()

print(retention,avg_order,freq)

