import numpy as np
import pandas as pd
import h5py as h5
import matplotlib.pyplot as plt

###---------------------------------------------------------
### Please modify the path for:
### 1. Price file
### 2. Prediction file
###---------------------------------------------------------
f = h5.File("/Users/dominicleung/Documents/4390Local/HKSTOCK4.hdf5", 'r') #Set the pointer object
label = pd.read_csv("/Users/dominicleung/Documents/4390Local/Market_Related/mr6_pred.csv")

###---------------------------------------------------------
### Predefined function
###---------------------------------------------------------
def resample(group):
    return group.resample('M').last()

def max_drawdown(X):
    mdd = 0
    peak = X[0]
    for x in X:
        if x > peak: 
            peak = x
        dd = (peak - x)
        if dd > mdd:
            mdd = dd
    return mdd    

def bt_df(f, label):
    """ Return the dataframe that matches holding return with prediction """
    label['Date'] = pd.to_datetime(label['Date'], format = "%Y-%m-%d")
    for i in range(len(label)): #Change label to match with naming convention of QUANDL
        ticker = label.iloc[i,0][:-10]
        if len(ticker)<5:
            for j in range(len(ticker),4):
                ticker = '0'+ticker
        ticker += " HK Equity"
        label.iloc[i,0] = ticker
    item_list = list(set(list(label['Ticker'])))
    label = label.set_index(['Date']).groupby('Ticker').resample('M').ffill()
    label.drop('Ticker', axis = 1, inplace = True)

    #Input data from hdf5
    new = True
    for item in item_list:
        try:
            stock = np.array(f[item])
            stock_df = pd.DataFrame(stock)
            stock_df['Ticker'] = item
            stock_df.dropna(inplace = True)
            if new:
                df = pd.DataFrame(columns = stock_df.columns)
                new = False
            df = df.append(stock_df.copy(deep = True), sort = False)
        except:
            print(item)
    #Resample data to monthly
    df['Date'] = pd.to_datetime(df['Date'].str.decode("utf-8"))
    df.set_index('Date', inplace = True)
    
    result = df.groupby('Ticker').apply(resample)
    result.drop(['Ticker'], axis = 1, inplace = True) #Duplicate columns that should be removed
    bt = pd.DataFrame(result.groupby('Ticker')['Adj Close'].pct_change().shift(-1)) #Make as the return if we long at that time
    bt.rename(columns = {"Adj Close": "Monthly Return"},  inplace = True)
    bt.reset_index(inplace = True)
    bt.set_index(['Ticker','Date'], inplace = True)
    #Resample data to monthly
    backtest = label.merge(bt, left_on = ['Ticker', 'Date'], right_on = ['Ticker', 'Date']).reset_index()

    return backtest

###---------------------------------------------------------
### THe final result
### Analysis starts at here
###---------------------------------------------------------
if __name__ == "__main__":
    backtest = bt_df(f, label)
    grp = {}
    for i in set(list(label.pred)):
        grp[i] = backtest.loc[backtest['pred']==i].groupby('Date')['Monthly Return'].mean()
    grp = pd.DataFrame(grp)

    #Plot the performance for each group
    plt.rcParams["figure.figsize"] = [10,5]
    grp.plot()

    # #Count number of stocks for each data
    grpcount = pd.DataFrame(backtest.groupby(['Date','pred'])['Ticker'].count())
    grpcount.groupby('pred')['Ticker'].plot()

    LS = (grp[7]- grp[1])
    LS.cumsum().plot(grid = True)
    total_ret = (LS.cumsum()[-1]/4)
    sharpe = (LS.cumsum()[-1]/4) / (LS.std()*np.sqrt(12))
    mdd = max_drawdown(LS.cumsum())
    print(f'Total Return: {total_ret}')
    print(f'Sharpe: {sharpe}')
    print(f'Maximum Drawdown: {mdd}')


###----------------------------------------
### Validation Set
###----------------------------------------




