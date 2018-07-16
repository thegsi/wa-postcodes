import pandas as pd
import numpy as np

# waPostcodesDf = pd.read_csv('./waPostcodesDateDf_aggregated.csv', sep=',', header=None, names=['postcodeDate', 'no', 'easting', 'northing'], dtype={'postcodeDate': 'object', 'no': 'object' }, index_col='postcodeDate')
waPostcodesDf = pd.read_csv('./waPostcodesDateDf_aggregated.csv', sep=',',index_col='postcodeDate')

waPostcodesDf['postcodeDate'] = waPostcodesDf.index

waPostcodesDf['date'] = waPostcodesDf['postcodeDate'].map(lambda x: x[-4:])
waPostcodesDf['postcode'] = waPostcodesDf['postcodeDate'].map(lambda x: x.split()[0])

# print(waPostcodesDf.iloc[1])
waPostcodesDf.to_csv('waPostcodesDf_aggregated_clean.csv')
