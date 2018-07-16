import csv
import pyproj
import pandas as pd
# import os

# files = os.listdir('./OS_postcodes/Data/CSV')
bng = pyproj.Proj(init='epsg:27700')
wgs84 = pyproj.Proj(init='epsg:4326')

# Process unknown postcodes
# if r[2][4] == ' ':
#     x = r[2].replace(' ', '')
#     r[2] = x

osPostcodesDf = pd.read_csv('./OS_postcodes/Data/CSV/ospostcodes.csv', header=None, usecols=[0, 2, 3], names=['postcode', 'easting', 'northing'], index_col=0)

# https://osedok.wordpress.com/2012/01/17/conversion-of-british-national-grid-wkid27700-to-wgs84wkid4326-and-then-to-webmercator-wkid102100/
osPostcodesDf['easting'], osPostcodesDf['northing'] = pyproj.transform(bng,wgs84,list(osPostcodesDf['easting']), list(osPostcodesDf['northing']))
# lon,lat = pyproj.transform(bng,wgs84,int(osDf.loc[r[2], 'easting']), int(osDf.loc[r[2], 'northing']))

osPostcodesDf.to_csv('OS_postcodes_latlong.csv')
