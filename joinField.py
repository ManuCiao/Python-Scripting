import arcpy
import os

arcpy.env.workspace = worksapce # insert workspace
sourceFC = "feature" #insert source feature class
joinField = "" # insert source Join Field
valueField = "" # insert the new field to join
updateFc = "" # insert the feature that will have added the new field
updateJoinField = "" # insert the common field that will be compared with the joinField from the source feature class

def joinFcToUpdBasinsTable(sourceFC, joinField, valueField, updateFc, updateJoinField):
    """Join feature classes to table"""
    sourceFields = [joinField, valueField]
    valueDict = {r[0]: (r[1:]) for r in arcpy.da.SearchCursor(sourceFC, sourceFields)}
    updateFields = [updateJoinField, valueField]

    arcpy.AddField_management(updateFc, valueField, "TEXT", "", "", 8)
    if valueField not in [f.name for f in arcpy.ListFields(updateFc)]:
        print "'{0}' not found in \"{1}\"".format(valueField, os.path.basename(updateFc))
        print 'Please verify that field name matches in "{}"'.format(os.path.basename(updateFc))
        sys.exit()
    else:
        with arcpy.da.UpdateCursor(updateFc, updateFields) as cursor:
            for row in cursor:
                keyValue = row[0]
                if keyValue in valueDict:
                    row[1] = valueDict[keyValue][0]
                    cursor.updateRow(row)
                else:
                    row[1] = 0
        print "Field {0} has been updated in {1}!".format(valueField, os.path.basename(updateFc))

joinFcToUpdBasinsTable(sourceFC, joinField, valueField, updateFc, updateJoinField)
