import csv

# https://stackoverflow.com/questions/17444679/reading-a-huge-csv-file
with open('./WA_postcodes/summary-count-year-postcode.tsv', 'rb') as postcodes:
    waPostcodesReader = csv.reader(postcodes, delimiter='\t')

    def createGeoRow():
        count = 0
        for r in waPostcodesReader:
            if count < 10:
                # Access the correct OS postcode file
                areaId = r[2][:2]
                if r[2][1].isdigit():
                    areaId = r[2][:1]

                osFilename = './OS_postcodes/Data/CSV/%s.csv' % areaId
                # Match the WA postcode with OS postcode
                # WA 7283565	2008	CV1 2EL
                # OS "BA1 0AQ",10,375350,164482,"E92000001","E19000002","E18000010","","E06000022","E05001935"
                with open(osFilename, 'rb') as osPostcodes:
                    osPostcodesReader = csv.reader(osPostcodes, delimiter=',')
                    for osRow in osPostcodesReader:
                        if osRow[0] == r[2]:
                            count += 1
                            # Create a new row
                            yield r + osRow[2:4]
            else:
                return

    for row in createGeoRow():
        print(row)
        # Create new csv file

        # yield new row to new csv file
        # https://stackoverflow.com/questions/49589983/bulk-create-fails-with-1-milion-rows
