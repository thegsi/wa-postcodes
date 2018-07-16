import pandas as pd
import numpy as np

waPostcodesDf = pd.read_csv('./WA_postcodes/summary-count-year-postcode.tsv', sep='\t', header=None, names=['no', 'date', 'postcode', 'easting', 'northing'], dtype={'no': 'object', 'date': 'object', 'postcode': 'object', 'long': 'float64', 'lat': 'float64' }, index_col='postcode')
osPostcodesDf = pd.read_csv('./OS_postcodes_latlong.csv', sep=',', usecols=[0, 1, 2], header=0, names=['postcode', 'easting', 'northing'], dtype={'postcode': 'object', 'easting': 'float64', 'northing': 'float64' }, index_col=0)

waIndex = waPostcodesDf.index
names = waIndex.names
waIndex = [pC.replace(' ', '') if len(pC) == 8 else pC for pC in waIndex]
# waPostcodesDf.index = pd.MultiIndex.from_tuples(waIndex, names = names)
waPostcodesDf.index = waIndex

waPostcodesDf.update(osPostcodesDf)

print('success')

waPostcodesDf.to_csv('waPostcodesDf.csv')
