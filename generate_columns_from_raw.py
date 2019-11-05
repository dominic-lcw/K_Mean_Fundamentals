import pandas as pd
import numpy as np
import h5py as h5

source = "/Users/dominicleung/Documents/4390Local/Bloomberg/Market_Related.csv"
df = pd.read_csv(source

col_name = df.columns
df = df.rename(columns = {col_name[0]:'Date', col_name[1]:'Ticker'})

length = len(df.columns)
for i in range(2,length):
    df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors = 'coerce')
df = df.groupby('Ticker').apply(lambda x: x.fillna(method = 'ffill'))

###PCT_Change 
drop_list = ['TRAIL_12M_EPS', 'EV_12M_OPER_INC']
chg_list = ['PX_TO_BOOK_RATIO','PX_TO_SALES_RATIO','PE_RATIO']
#chg_list = ['PX_TO_BOOK_RATIO','PX_TO_SALES_RATIO','PE_RATIO']
for item in drop_list:
    df[(item+"_chg_lag1")] = df.groupby('Ticker')[item].pct_change()
for item in chg_list:
    df[(item+"_chg_lag1")] = df.groupby('Ticker')[item].pct_change()
df.drop(drop_list, axis = 1, inplace = True)

###PCT_Change lag2
chg_list = ['PX_TO_BOOK_RATIO','PX_TO_SALES_RATIO','PE_RATIO']
#chg_list = ['PX_TO_BOOK_RATIO','PX_TO_SALES_RATIO','PE_RATIO']
for item in (chg_list):
    df[(item+"_chg_lag2")] = df.groupby('Ticker')[item].pct_change(2)

###Normalize
df.set_index(['Ticker','Date'], inplace =True)
df = df.groupby('Date').transform(lambda x: (x-x.mean())/x.std())
df =df.replace([np.inf, -np.inf], np.nan)

###Winsorize
names = df.columns
for item in names:
    df.loc[df[item]>2, item] = 2
    df.loc[df[item]<-2, item] = -2

df.dropna(inplace = True)
df.count()


#Tradable List
tradable = pd.read_csv(trade, header = None)
col_name = tradable.columns
tradable = tradable.rename(columns = {col_name[0]:'Ticker', col_name[1]:'Date'})
tradable['Date'] = pd.to_datetime(tradable['Date'], format = '%Y%m%d')
tradable.head()

#Information
df.reset_index(inplace = True)
df['Date'] = pd.to_datetime(df['Date'], format = "%Y%m%d")
df.head()

#Left Merge
result = pd.merge(tradable, df, left_on = ['Ticker','Date'], right_on = ['Ticker','Date'], how = 'left')
result.dropna(inplace = True)

#Training Dataset and Validation Dataset
tr = result.loc[result['Date']<'2018']
vl = result.loc[result['Date']>='2018']


#Output the file
fl_name = "mr1.csv"
train_target = "/Users/dominicleung/Documents/4390Local/Market_Related/Training/"+fl_name
val_target = "/Users/dominicleung/Documents/4390Local/Market_Related/Validation/"+fl_name
tr.to_csv(train_target, index = False)
vl.to_csv(val_target, index = False)