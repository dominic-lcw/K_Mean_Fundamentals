import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

###---------------------------------------------------------
### Please modify the path for:
### 1. Source File
### 2. Target path for the stored results
###---------------------------------------------------------
source = "/Users/dominicleung/OneDrive/Documents/FINA4390/industry/hk5mil.csv"
target = "/Users/dominicleung/OneDrive/Documents/FINA4390/industry/4390_7th_cleaned.csv"

def clean_data(source, target):
	'''Clean data by removing NA
	'''
	df = pd.read_csv(source)

	#Change Column names
	col_name = df.columns
	df = df.rename(columns = {col_name[0]:'Ticker', col_name[1]:'Date'})

	length = len(df.columns)
	for i in range(2,length):
	    df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors = 'coerce')
	df = df.groupby('Ticker').apply(lambda x: x.fillna(method = 'ffill'))

	###PCT_Change 
	df['NET_SALES_PCT_CHANGE'] = df.groupby('Ticker')['TRAIL_12M_NET_SALES'].pct_change()
	df['NET_FIX_ASSET_TURN_PCT_CHANGE'] = df.groupby('Ticker')['NET_FIX_ASSET_TURN'].pct_change()
	df['INVENT_TURN_PCT_CHANGE'] = df.groupby('Ticker')['INVENT_TURN'].pct_change()
	df.drop(['TRAIL_12M_NET_SALES','NET_FIX_ASSET_TURN','INVENT_TURN'], axis = 1, inplace = True)

	###Normalize
	df = df.groupby('Date').transform(lambda x: (x-x.mean())/x.std())
	df =df.replace([np.inf, -np.inf], np.nan)
	df.dropna(inplace = True)

	###Winsorize
	names = df.columns
	for i in range(2,length):
	    df.loc[df[names[i]]>2, names[i]] = 2
	    df.loc[df[names[i]]<-2, names[i]] = -2

	df.to_csv(target, index = False)

if __name__ == "__main__":
	clean_data(source, target)

