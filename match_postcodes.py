import csv
import pyproj
import pandas as pd

bng = pyproj.Proj(init='epsg:27700')
wgs84 = pyproj.Proj(init='epsg:4326')

# https://stackoverflow.com/questions/17444679/reading-a-huge-csv-file
with open('./WA_postcodes/summary-count-year-postcode.tsv') as postcodes:
    waPostcodesReader = csv.reader(postcodes, delimiter='\t')

    def createGeoRow():
        count = 0
        for r in waPostcodesReader:
            if count < 1000:
                # Access the correct OS postcode file
                areaId = r[2][:2]
                if r[2][1].isdigit():
                    areaId = r[2][:1]

                osFilename = './OS_postcodes/Data/CSV/%s.csv' % areaId
                # Match the WA postcode with OS postcode
                # WA 7283565	2008	CV1 2EL
                # OS "BA1 0AQ",10,375350,164482,"E92000001","E19000002","E18000010","","E06000022","E05001935"
                try:
                    count += 1
                    osDf = pd.read_csv(osFilename, header=None, usecols=[0, 2, 3], names=['postcode', 'easting', 'northing'], index_col=0)
                    if r[2][4] == ' ':
                        x = r[2].replace(' ', '')
                        r[2] = x

                    # https://osedok.wordpress.com/2012/01/17/conversion-of-british-national-grid-wkid27700-to-wgs84wkid4326-and-then-to-webmercator-wkid102100/
                    lon,lat = pyproj.transform(bng,wgs84,int(osDf.loc[r[2], 'easting']), int(osDf.loc[r[2], 'northing']))
                    # Create a new row
                    yield r + [lon, lat]

                    # csv version
                    # with open(osFilename) as osPostcodes:
                    #     osPostcodesReader = csv.reader(osPostcodes, delimiter=',')
                    #     for osRow in osPostcodesReader:
                    #         if osRow[0] == r[2]:
                    #             count += 1
                    #             # https://osedok.wordpress.com/2012/01/17/conversion-of-british-national-grid-wkid27700-to-wgs84wkid4326-and-then-to-webmercator-wkid102100/
                    #             lon,lat = pyproj.transform(bng,wgs84,int(osRow[2]), int(osRow[3]))
                    #             # Create a new row
                    #             yield r + [lon, lat]
                except:
                    print('postcode unknown')
            else:
                return

    # Create new csv file
    latLongCsv = csv.writer(open('latLongCsv.csv','w'), delimiter=',',quoting=csv.QUOTE_ALL)

    for row in createGeoRow():
        # yield new row to new csv file
        # https://stackoverflow.com/questions/49589983/bulk-create-fails-with-1-milion-rows
        latLongCsv.writerow(row)
        print(row)
