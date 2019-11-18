import numpy as np
import pandas as pd
import h5py as h5
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

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

def bt_train_df(f, label):
    ''' Merge the return for the each stocks in the dataframe
    :param f: object for hdf5 file
    :param label: dataframe for the label file
    
    :returns: dataframe with monthly return for each stocks
    '''

    #Change label to match with naming convention of QUANDL
    for i in range(len(label)): 
        ticker = label.iloc[i,0][:-10]
        if len(ticker)<5:
            for j in range(len(ticker),4):
                ticker = '0'+ticker
        ticker += " HK Equity"
        label.iloc[i,0] = ticker

    #Adjusting the time index
    label['Date'] = pd.to_datetime(label['Date'], format = "%Y-%m-%d")
    ticker_list = list(set(list(label['Ticker'])))
    label.set_index(['Ticker', 'Date'], inplace = True)
    label.sort_index(inplace = True)
    for ticker in ticker_list:
        d = label.loc[ticker].index[-1]#+timedelta(181)
        s = label.xs([ticker,d])
        s.name = (ticker,d+timedelta(181))
        label = label.append(s)
    
    #Change from semi-annual to monthly
    label.sort_index(inplace = True) #Resort the dataframe again
    label.reset_index(inplace = True)
    label = label.set_index(['Date']).groupby('Ticker').resample('M').ffill()
    label.drop('Ticker', axis = 1, inplace = True)

    #Convert the price hdf5 to a large dataframe
    new = True
    for item in ticker_list:
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

    #Resample daily data to monthly
    df['Date'] = pd.to_datetime(df['Date'].str.decode("utf-8"))
    df.set_index('Date', inplace = True)
    result = df.groupby('Ticker').apply(resample)
    result.drop(['Ticker'], axis = 1, inplace = True) #Duplicate columns that should be removed
    
    #Calculate return for each stock, each month
    ret = pd.DataFrame(result.groupby('Ticker')['Adj Close'].pct_change().shift(-1)) #Make as the return if we long at that time
    ret.rename(columns = {"Adj Close": "Monthly Return"},  inplace = True)
    
    #Merge the label dataframe with the return dataframe
    backtest = label.merge(ret, left_on = ['Ticker', 'Date'], right_on = ['Ticker', 'Date'])
    backtest = backtest.groupby('Ticker').shift(1)
    backtest['pred'] = backtest['pred'].fillna(method = 'bfill')
    backtest = backtest.fillna(0)

    return backtest

def bt_val_df(f, label):
    ''' Merge the return for the each stocks in the dataframe
    :param f: object for hdf5 file
    :param label: dataframe for the label file
    
    :returns: dataframe with monthly return for each stocks
    '''

    #Change label to match with naming convention of QUANDL
    for i in range(len(label)): 
        ticker = label.iloc[i,0][:-10]
        if len(ticker)<5:
            for j in range(len(ticker),4):
                ticker = '0'+ticker
        ticker += " HK Equity"
        label.iloc[i,0] = ticker

    #Adjusting the time index
    label['Date'] = pd.to_datetime(label['Date'], format = "%Y-%m-%d")
    ticker_list = list(set(list(label['Ticker'])))
    label.set_index(['Ticker', 'Date'], inplace = True)
    label.sort_index(inplace = True)
    for ticker in ticker_list:
        d = label.loc[ticker].index[-1]#+timedelta(181)
        s = label.xs([ticker,d])
        s.name = (ticker,d+timedelta(181))
        label = label.append(s)
    
    #Change from semi-annual to monthly
    label.sort_index(inplace = True) #Resort the dataframe again
    label.reset_index(inplace = True)
    label = label.set_index(['Date']).groupby('Ticker').resample('M').ffill()
    label.drop('Ticker', axis = 1, inplace = True)

    #Convert the price hdf5 to a large dataframe
    new = True
    for item in ticker_list:
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

    #Resample daily data to monthly
    df['Date'] = pd.to_datetime(df['Date'].str.decode("utf-8"))
    df.set_index('Date', inplace = True)
    result = df.groupby('Ticker').apply(resample)
    result.drop(['Ticker'], axis = 1, inplace = True) #Duplicate columns that should be removed
    
    #Calculate return for each stock, each month
    ret = pd.DataFrame(result.groupby('Ticker')['Adj Close'].pct_change().shift(-1)) #Make as the return if we long at that time
    ret.rename(columns = {"Adj Close": "Monthly Return"},  inplace = True)
    
    #Merge the label dataframe with the return dataframe
    backtest = label.merge(ret, left_on = ['Ticker', 'Date'], right_on = ['Ticker', 'Date'])
    backtest = backtest.groupby('Ticker').shift(1)
    backtest['v_pred'] = backtest['v_pred'].fillna(method = 'bfill')
    backtest = backtest.fillna(0)

    return backtest

def grp_train_return(backtest, label):
    '''Obtain the grouped return from the backtest file
    '''
    grp = {}
    for i in set(list(label.pred)):
        grp[i] = backtest.loc[backtest['pred']==i].groupby('Date')['Monthly Return'].mean()
    
    return(pd.DataFrame(grp))

def grp_val_return(backtest, label):
    '''Obtain the grouped return from the backtest file
    '''
    grp = {}
    for i in set(list(label.v_pred)):
        grp[i] = backtest.loc[backtest['v_pred']==i].groupby('Date')['Monthly Return'].mean()
    
    return(pd.DataFrame(grp))

###---------------------------------------------------------
### THe final result
### Analysis starts at here
###---------------------------------------------------------
if __name__ == "__main__":
    #Set the pointer object
    f = h5.File("/Users/dominicleung/Documents/4390Local/HKSTOCK6.hdf5", 'r') 
    label = pd.read_csv("/Users/dominicleung/Documents/4390Local/Market_Related/mr7_pred.csv")
    train = bt_train_df(f, label)
    t_grp = grp_train_return(train, label)

    #Plot the performance for each group
    plt.rcParams["figure.figsize"] = [10,5]
    t_grp.plot()

    # #Count number of stocks for each data
    grpcount = pd.DataFrame(train.reset_index().groupby(['Date','pred'])['Ticker'].count())
    grpcount.reset_index().set_index('Date').groupby('pred')['Ticker'].plot()

    LS = (t_grp[7]- t_grp[1])
    LS.cumsum().plot(grid = True)

    #General backtesting stat
    nyears = relativedelta(t_grp.index[-1], t_grp.index[1])
    years =nyears.years + nyears.months/12
    total_ret = (LS.cumsum()[-1]/years)
    sharpe = (LS.cumsum()[-1]/years) / (LS.std()*np.sqrt(12))
    mdd = max_drawdown(LS.cumsum())
    print(f'Time Length (years):{round(years,2)}')
    print(f'Annual Return: {total_ret}')
    print(f'Sharpe: {sharpe}')
    print(f'Maximum Drawdown: {mdd}')

###----------------------------------------
### Validation Set
###----------------------------------------
    f = h5.File("/Users/dominicleung/Documents/4390Local/HKSTOCK6.hdf5", 'r') #Set the pointer object
    label = pd.read_csv("/Users/dominicleung/Documents/4390Local/Market_Related/mr7_val.csv")
    val = bt_val_df(f, label)
    v_grp = grp_val_return(val,label)

    #Plot the performance for each group
    plt.rcParams["figure.figsize"] = [10,5]
    t_grp.plot()

    grpcount = pd.DataFrame(val.reset_index().groupby(['Date','v_pred'])['Ticker'].count())
    grpcount.reset_index().set_index('Date').groupby('pred')['Ticker'].plot()

    v_LS = (v_grp[1]-v_grp[2])
    v_LS.cumsum().plot(grid = True)

    #General backtesting stat
    nyears = relativedelta(v_grp.index[-1], v_grp.index[1])
    years =nyears.years + nyears.months/12
    total_ret = (v_LS.cumsum()[-1]/years)
    sharpe = (v_LS.cumsum()[-1]/years) / (v_LS.std()*np.sqrt(12))
    mdd = max_drawdown(v_LS.cumsum())
    print(f'Time Length (years):{round(years,2)}')
    print(f'Annual Return: {total_ret}')
    print(f'Sharpe: {sharpe}')
    print(f'Maximum Drawdown: {mdd}')
