import pandas as pd
import numpy as np

waPostcodesDf = pd.read_csv('./WA_postcodes/summary-count-year-postcode.tsv', sep='\t', header=None, names=['no', 'date', 'postcode', 'easting', 'northing'], dtype={'no': 'object', 'date': 'object', 'postcode': 'object', 'long': 'float64', 'lat': 'float64' }, index_col='postcode')

waIndex = waPostcodesDf.index
waPostcodesDf['postcodeShort'] = [pC[:5] if len(pC) == 8 else pC[:4] for pC in waIndex]
waPostcodesDf['postcodeDate'] = waPostcodesDf['postcodeShort'] + waPostcodesDf['date']

waPostcodesDf['no'] = pd.to_numeric(waPostcodesDf['no'], errors='coerce').fillna(0).astype(np.int64)

waPostcodesDateSeries = waPostcodesDf.groupby(by=['postcodeDate'])['no'].sum()

waPostcodesDateDf = pd.DataFrame({'postcodeDate':waPostcodesDateSeries.index, 'no':waPostcodesDateSeries.values})

waPostcodesDateDf = waPostcodesDateDf[waPostcodesDateDf['no'] != 0]

# print(waPostcodesDateDf)

waPostcodesDateDf.to_csv('waPostcodesDateDf_aggregated.csv')
