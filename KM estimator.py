import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines import NelsonAalenFitter

df=pd.read_csv('subs.txt',sep='\t',encoding='ISO-8859-1',parse_dates=['start_date','stop_date'])
df = df.loc[(df.tenure >= 0) & (df.start_date >= '2004-01-01')]
df['churned'] = df['stop_type'].apply(lambda x : 0 if pd.isnull(x) else 1)
naf = NelsonAalenFitter()
naf.fit(durations=df['tenure'],event_observed = df['churned'])
#CDF harzard
print(naf.cumulative_hazard_)
naf.plot_cumulative_hazard()


kmf = KaplanMeierFitter()
kmf.fit(durations=df['tenure'],event_observed = df['churned'])
print(kmf.survival_function_)
kmf.plot_survival_function()
plt.show()