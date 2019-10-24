import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

###---------------------------------------------------------
### Please modify the path for:
### 1. Source File
### 2. Target path for the stored results
###---------------------------------------------------------
source = "/Users/dominicleung/Documents/4390Local/Market_Related.csv"
train_target = "/Users/dominicleung/Documents/4390Local/Training/TMarket_Related.csv"
val_target = "/Users/dominicleung/Documents/4390Local/Validation/VMarket_Related.csv"

def clean_data(source, train_target, val_target):
	'''Clean data by removing NA
	'''
	###Correctly Read the Data
	df = pd.read_csv(source)
	col_name = df.columns
	df = df.rename(columns = {col_name[0]:'Ticker', col_name[1]:'Date'})

	###Ffill
	length = len(df.columns)
	for i in range(2,length):
	    df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors = 'coerce')
	df = df.groupby('Ticker').apply(lambda x: x.fillna(method = 'ffill'))

	###PCT_Change 
	drop_list = ['TRAIL_12M_EPS']
	chg_list= ['ASSET_TURNOVER','INVENT_TURN','ACCT_RCV_TURN',
	'NET_FIX_ASSET_TURN','ACCOUNTS_PAYABLE_TURNOVER']
	for item in (drop_list+chg_list):
    	df[(item+'_chg')] = df.groupby('Ticker')[item].pct_change()
	df.drop(drop_list, axis = 1, inplace = True)

	###Normalize
	df.set_index(['Ticker','Date'], inplace =True)
	df = df.groupby('Date').transform(lambda x: (x-x.mean())/x.std())
	df =df.replace([np.inf, -np.inf], np.nan)
	df.dropna(inplace = True)

	###Winsorize
	names = df.columns
	for item in names:
	    df.loc[df[item]>2, item] = 2
	    df.loc[df[item]<-2, item] = -2

	###Splitting Dataset
	df.reset_index(inplace = True)
	df['Date'] = pd.to_datetime(df['Date'], format = "%Y%m%d")
	tr = df.loc[df['Date']<'2018']
	vl = df.loc[df['Date']>='2018']


	tr.to_csv(train_target, index = False)
	vl.to_csv(val_target, index = False)

if __name__ == "__main__":
	clean_data(source, train_target, val_target)

