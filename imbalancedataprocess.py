import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

ds_model = pd.read_csv('ds_model.txt',sep=',')
ds_pred = pd.read_csv('ds_pred.txt',sep=',')
ds_model = ds_model[['householdid','recency','monetary','frequency','clv']]
# print(ds_model.clv.isnull().sum())
# print(ds_model.clv.shape)
ds_model['churned'] = ds_model['clv'].apply(lambda x:True if np.isnan(x) else False)
# print(ds_model['churned'].value_counts())
X_train,X_test,y_train,y_test = train_test_split(ds_model[['recency','monetary','frequency']],
                                                 ds_model['churned'],test_size=0.33,random_state=42)
logistic = LogisticRegression(random_state=0,class_weight='balanced').fit(X_train,y_train)
y_pred = logistic.predict(X_test)
y_test = y_test.to_frame(name='test')
y_test['pred'] = y_pred
print(y_test['test'].value_counts())
print(y_test['pred'].value_counts())


from sklearn.tree import DecisionTreeClassifier

tree = DecisionTreeClassifier(random_state=0).fit(X_train,y_train)
tree_pred = tree.predict(X_test)
y_test['tree_pred'] = tree_pred
print(y_test['tree_pred'].value_counts())