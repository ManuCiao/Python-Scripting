import arcpy

arcpy.env.workspace = r"D:\Users\test.gdb"
infeature = "feature"  # insert the feature class
field_in = "field"  # insert the field of the feature class
field_out = "DUPLICATES_" + field_in

# create the field for the count values
arcpy.AddField_management(infeature, field_out, "SHORT")

# creating the list with all the values in the field, including duplicates
field_list = []
cursor1 = arcpy.SearchCursor(infeature)
for row in cursor1:
    i = row.getValue(field_in)
    field_list.append(i)
del cursor1, row

# updating the count field with the number on occurrences of field_in values
# in the previously created list
cursor2 = arcpy.UpdateCursor(infeature)
for row in cursor2:
    i = row.getValue(field_in)
    occ = field_list.count(i)
    row.setValue(field_out, occ)
    cursor2.updateRow(row)
del cursor2, row
print ("The duplicates field has been updated.")
