import numpy as np
import pandas as pd
import h5py as h5
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import backtest as bt

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

def label_csv(source):
    label = pd.read_csv(source)
    label['Date'] = pd.to_datetime(label['Date'], format = "%Y-%m-%d")
    for i in range(len(label)): 
        ticker = label.iloc[i,0][:-10]
        if len(ticker)<5:
            for j in range(len(ticker),4):
                ticker = '0'+ticker
        ticker += " HK Equity"
        label.iloc[i,0] = ticker
    return label


def return_df(f, label):
    #Get the ticker list
    ticker_list = list(set(list(label['Ticker'])))

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
    
    return ret


def bt_df(ret, label):
    ''' Merge the return for the each stocks in the dataframe
    :param f: object for hdf5 file
    :param label: dataframe for the label file
    
    :returns: dataframe with monthly return for each stocks
    '''

    #Get the date and ticker
    d = list(set(list(label['Date'])));d.sort();d.append(d[-1]+ timedelta(181))
    t = list(set(list(label['Ticker'])))

    #Construct a dummy dataframe
    ts = pd.DataFrame(index=pd.MultiIndex.from_product([t, d],
        names = ['Ticker','Date']))

    #Merge the dummy with label dataframe
    mlabel = ts.merge(label.set_index(['Ticker','Date'])['pred'], 
        left_on = ['Ticker','Date'],right_on = ['Ticker','Date'], 
        how = 'left')
    mlabel = mlabel.fillna(99)

    #Resample to monthly
    mlabel = mlabel.reset_index().set_index('Date').groupby('Ticker').resample('M').last()
    mlabel.drop('Ticker',axis = 1, inplace = True)
    mlabel = mlabel.groupby('Ticker').fillna(method = 'ffill')

    #Merge the label dataframe with the return dataframe
    backtest = mlabel.merge(ret, 
        left_on = ['Ticker', 'Date'], right_on = ['Ticker', 'Date'], 
        how = 'left')
    backtest = backtest.groupby('Ticker').shift(1)
    backtest['pred'] = backtest['pred'].fillna(method = 'bfill')
    backtest = backtest.fillna(0)

    return backtest

def grp_return(backtest, label):
    '''Obtain the grouped return from the backtest file
    '''
    grp = {}
    for i in set(list(label.pred)):
        grp[i] = backtest.loc[backtest['pred']==i].groupby('Date')['Monthly Return'].mean()
    
    return(pd.DataFrame(grp))


###---------------------------------------------------------
### THe final result
### Analysis starts at here
###---------------------------------------------------------
if __name__ == "__main__":
    #Set the pointer object
    f = h5.File("/Users/dominicleung/Documents/4390Local/HKSTOCK6.hdf5", 'r') 
    
    #Backtesting object
    label = bt.label_csv("/Users/dominicleung/Documents/4390Local/Market_Related/mr7_pred.csv")
    r = bt.return_df(f, label)
    train = bt.bt_df(r, label)
    t_grp = bt.grp_return(train, label)

    #Plot the performance for each group
    plt.rcParams["figure.figsize"] = [10,5]
    t_grp.plot(grid = True);

    # #Count number of stocks for each data
    grpcount = pd.DataFrame(train.reset_index().groupby(['Date','pred'])['Ticker'].count())
    grpcount.reset_index().set_index('Date').groupby('pred')['Ticker'].plot(legend = True);

    LS = (t_grp[1]- t_grp[2])
    LS.cumsum().plot(grid = True);

    #General backtesting stat
    nyears = relativedelta(t_grp.index[-1], t_grp.index[1])
    years =nyears.years + nyears.months/12
    total_ret = (LS.cumsum()[-1]/years)
    sharpe = (LS.cumsum()[-1]/years) / (LS.std()*np.sqrt(12))
    mdd = bt.max_drawdown(LS.cumsum())
    print(f'Time Length (years):{round(years,2)}')
    print(f'Annual Return: {total_ret}')
    print(f'Sharpe: {sharpe}')
    print(f'Maximum Drawdown: {mdd}')
