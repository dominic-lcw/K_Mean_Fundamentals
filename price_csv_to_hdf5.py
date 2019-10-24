import hdf5 as h5
import pandas as pd
import numpy as np
import glob

path = "/Users/dominicleung/Documents/4390Local/price_csv/output/*.csv"
f = h5.File("/Users/dominicleung/Documents/4390Local/HKSTOCK4.hdf5", 'w')

for fname in glob.glob(path):
    df = pd.read_csv(fname)
    name = fname[-11:-7]+" HK Equity"
    d = df.to_records(index = False, column_dtypes = {'Date': 'S10'})
    f.create_dataset(name, data = d)

f.close()
