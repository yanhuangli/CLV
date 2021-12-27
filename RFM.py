import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df_order = pd.read_csv('orders.txt',sep='\t',encoding='ISO-8859-1',parse_dates=['orderdate'])
df_customer = pd.read_csv('customer.txt',sep='\t',encoding='ISO-8859-1')


df_order = df_order[['orderid','customerid','orderdate','totalprice',]]

df_customer = df_customer[['customerid','householdid']]
df = pd.merge(df_order,df_customer,on='customerid')
household_order = df.groupby('householdid').agg({'orderid':lambda x:len(x)})
#calculate recency
df_1 = df.groupby('householdid').orderdate.max().reset_index()
df_1.columns = [['householdid','max_date']]
df_1['rencency'] = (df_1.max_date.max()-df_1.max_date).apply(lambda x:x.dt.days)
# print(df_1)

# plt.hist(df_1['rencency'])
# plt.show()
# elbow = {}
# for x in range(1,10):
#     kmeans = KMeans(n_clusters=x,random_state=0).fit(df_1['rencency'].to_numpy())
#     #define clusters
#     df_1['cluster'] = kmeans.labels_
#     #fine inertia for defining best N clusters
#     elbow[x] = kmeans.inertia_
# #
# plt.plot(elbow.keys(),elbow.values())
# plt.show()
#best N appear in N = 4
kmeans = KMeans(n_clusters=4,random_state=0).fit(df_1['rencency'].to_numpy())
df_1['rencency_cluster']= kmeans.predict(df_1['rencency'].to_numpy())
# print(df_1)

#delete multiindex returns
df_1.columns = df_1.columns.get_level_values(0)

#make cluster become ordinal

df_new = df_1.groupby('rencency_cluster')['rencency'].mean().reset_index()
df_new = df_new.sort_values(by='rencency',ascending=True).reset_index(drop=True)
df_new['Index'] = df_new.index
df_final = pd.merge(df_1,df_new[['rencency_cluster','Index']],on='rencency_cluster')
df_final = df_final.drop(['rencency_cluster'],axis=1)
#reset columns' name
df_final = df_final.rename(columns = {'Index':'rencency_cluster'})
print(df_final)