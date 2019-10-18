import numpy as np
import pandas as pd
import h5py as h5
import matplotlib.pyplot as plt

###---------------------------------------------------------
### Please modify the path for:
### 1. Price file
### 2. Prediction file
###---------------------------------------------------------
f = h5.File("/Users/dominicleung/OneDrive/Documents/FINA4390/stockprice/HKSTOCK3.hdf5", 'r') #Set the pointer object
label = pd.read_csv('/Users/dominicleung/OneDrive/Documents/FINA4390/industry/PE_NDE.csv')

###---------------------------------------------------------
### Predefined function
###---------------------------------------------------------
def resample(group):
    return group.resample('M').last()

def bt_df(f, label):
    """ Return the dataframe that matches holding return with prediction """
    item_list = list(f.keys())
    #Input data from hdf5
    new = True
    count = 0
    for item in item_list:
        stock = np.array(f[item])
        stock_df = pd.DataFrame(stock)
        if new:
            df = pd.DataFrame(columns = stock_df.columns)
            new = False
        df = df.append(stock_df.copy(deep = True), sort = False)
        count +=1
        if count % 100 ==0:
            print(count)

    #Resample data to monthly
    df['Date'] = pd.to_datetime(df['Date'].str.decode("utf-8"))
    df['Ticker'] = df['Ticker'].str.decode("utf-8")
    df.set_index('Date', inplace = True)
    result = df.groupby('Ticker').apply(resample)
    result.drop(['Ticker'], axis = 1, inplace = True) #Duplicate columns that should be removed
    bt = pd.DataFrame(result.groupby('Ticker')['Nominal Price'].pct_change().shift(-1)) #Make as the return if we long at that time
    bt.rename(columns = {"Nominal Price": "Monthly Return"},  inplace = True)
    bt.reset_index(inplace = True)
    bt.set_index(['Ticker','Date'], inplace = True)

    #Modify prediction file
    label['Date'] = pd.to_datetime(label['Date'], format = "%Y%m%d")
    for i in range(len(label)): #Change label to match with naming convention of QUANDL
        ticker = label.iloc[i,1][:-10]
        if len(ticker)<5:
            for j in range(len(ticker),5):
                ticker = '0'+ticker
        ticker = 'HKEX/'+ticker
        label.iloc[i,1] = ticker
    label = label.set_index(['Date']).groupby('Ticker').resample('M').ffill()
    label.drop('Ticker', axis = 1, inplace = True)
    backtest = label.merge(bt, left_on = ['Ticker', 'Date'], right_on = ['Ticker', 'Date']).reset_index()

    return backtest

###---------------------------------------------------------
### THe final result
### Analysis starts at here
###---------------------------------------------------------
if __name__ == "__main__":
    backtest = bt_df(f, label)
    grp = pd.DataFrame()
    for i in set(list(label.pred)):
        grp[i] = backtest.loc[backtest['pred']==i].groupby('Date')['Monthly Return'].mean()

    #Plot the performance for each group
    plt.rcParams["figure.figsize"] = [10,5]
    grp.plot()
    plt.show()

    # #Count number of stocks for each data
    grpcount = pd.DataFrame(backtest.groupby(['Date','pred'])['Ticker'].count())
    grpcount.groupby('pred')['Ticker'].plot()
    plt.show()








