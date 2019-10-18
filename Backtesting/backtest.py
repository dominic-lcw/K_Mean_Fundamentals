import numpy as np
import pandas as pd
import h5py as h5

price = "/Users/dominicleung/OneDrive/Documents/FINA4390/stockprice/HKSTOCK3.hdf5"
f = h5.File(price, 'r') #Set the pointer object
label = pd.read_csv('/Users/dominicleung/OneDrive/Documents/FINA4390/industry/PE_NDE.csv')

def resample(group):
    return group.resample('M').last()

item_list = list(f.keys())
#Input data
new = True
count = 1
for item in item_list:
    stock = np.array(f[item])
    stock_df = pd.DataFrame(stock)
    if new:
        df = pd.DataFrame(columns = stock_df.columns)
        new = False
    df = df.append(stock_df.copy(deep = True), sort = False)
    count+=1

df['Date'] = pd.to_datetime(df['Date'].str.decode("utf-8"))
df['Ticker'] = df['Ticker'].str.decode("utf-8")

df.set_index('Date', inplace = True)
result = df.groupby('Ticker').apply(resample)
result.drop(['Ticker'], axis = 1, inplace = True)
bt = pd.DataFrame(result.groupby('Ticker')['Nominal Price'].pct_change().shift(-1))
bt.rename(columns = {"Nominal Price": "Monthly Return"},  inplace = True)
bt.reset_index(inplace = True)
bt.set_index(['Ticker','Date'], inplace = True)

label['Date'] = pd.to_datetime(label['Date'], format = "%Y%m%d")
#Handle Label
for i in range(len(label)):
    ticker = label.iloc[i,1][:-10]
    if len(ticker)<5:
        for j in range(len(ticker),5):
            ticker = '0'+ticker
    ticker = 'HKEX/'+ticker
    label.iloc[i,1] = ticker
label = label.set_index(['Date']).groupby('Ticker').resample('M').ffill()
label.drop('Ticker', axis = 1, inplace = True)
backtest = label.merge(bt, left_on = ['Ticker', 'Date'], right_on = ['Ticker', 'Date'])
backtest.reset_index(inplace = True)
grp1 = backtest.loc[backtest['pred']==1].groupby('Date')['Monthly Return'].mean()
grp2 = backtest.loc[backtest['pred']==2].groupby('Date')['Monthly Return'].mean()
grp3 = backtest.loc[backtest['pred']==3].groupby('Date')['Monthly Return'].mean()
pplt123 = pd.DataFrame({'grp1':grp1,'grp2':grp2,'grp3':grp3})
pplt123.plot();

pd.DataFrame({'grp1c':grp1c,'grp2c':grp2c,'grp3c':grp3c}).plot()
