import arcpy

fc = r''  # add feature class/shapefile/table
field = ""  # add Field where to remove the NULL values
whereClause = field + " IS NULL"
updCurs = arcpy.UpdateCursor(fc, whereClause)
for row in updCurs:
    if not row.getValue(field):
        updCurs.deleteRow(row)

print "Process completed"
