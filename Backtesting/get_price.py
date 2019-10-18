import quandl
import pandas as pd
import numpy as np
import h5py as h5


quandl.ApiConfig.api_key = ""
source_doc = "/Users/dominicleung/OneDrive/Documents/FINA4390/industry/4390_5th_cleaned.csv"
stock = pd.read_csv(source_doc)  #Read CSV
target_doc = "HKSTOCK3.hdf5"
F = h5.File(target_doc, 'w')

###---------------------------------------
### Convert Name
###---------------------------------------
l = list(set(stock.iloc[:,1]))  #Name List
l = [name[:-10] for name in l]
for i in range(len(l)):
    if len(l[i]) <5:
        for j in range(len(l[i]),5):
            l[i] = '0'+l[i]
    l[i] = 'HKEX/'+l[i]

###---------------------------------------
### Convert Name
###---------------------------------------
count = 1
ex = []
for name in l:
    try:
        data = quandl.get(name, start_date='2015-01-01', end_date='2019-09-30')
        data.drop(['P/E(x)'], axis = 1, inplace = True)
        data['Ticker'] = name
        data.reset_index(inplace = True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        d = data.to_records(index = False, column_dtypes = {'Date': 'S10', 'Ticker': 'S10'})
        F.create_dataset(name[5:], data = d)
        if count %30 ==0:
            print(count)
        count +=1
    except Exception as e:
        ex.append(name)
        print(name)

F.close()








