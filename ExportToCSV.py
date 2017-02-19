import os
import arcpy
import csv

def dbf2csv(dbfpath, csvpath):
    # To convert .dbf file or any shapefile/featureclass to csv file
    # Inputs:
    #     dbfpath: full path to .dbf file [input] or featureclass
    #     csvpath: full path to .csv file [output]
    #import csv
    rows = arcpy.SearchCursor(dbfpath)
    csvFile = csv.writer(open(csvpath, 'wb')) #output csv
    fieldnames = [f.name for f in arcpy.ListFields(dbfpath)]

    allRows = []
    for row in rows:
        rowlist = []
        for field in fieldnames:
            rowlist.append(row.getValue(field))
        allRows.append(rowlist)

    csvFile.writerow(fieldnames)
    for row in allRows:
        csvFile.writerow(row)
    row = None
    rows = None

dbf_dir = 'S:/output_tables/'  # insert your dbf or shp/feature class directory
csv_dir = 'S:/output_tables/csv1/'  # insert your csv directory
for dbf_file in os.listdir(dbf_dir):
    # Loop through all dbf files
    # and export to dbf
    fileName, fileExt = os.path.splitext(dbf_file)  #[0] or [1] for file
    if '.dbf' in fileExt:
        # construct full path to dbf file and csv file
        dbfpath = os.path.join(dbf_dir, fileName+fileExt)
        csvpath = os.path.join(csv_dir, fileName+'.csv')
        if os.path.exists(dbfpath):
            # this may not be necessary
            #    print 'processing: ', dbfpath, csvpath
            if not os.path.exists(csvpath):
                ## to prevent overwrite of existing csv file
                ## call the function to convert .dbf file to csv file
                print 'Export nexrad {0} to {1}'.format(dbfpath, csvpath)
                dbf2csv(dbfpath, csvpath)
