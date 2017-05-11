import arcpy
import os

arcpy.env.workspace = r"D:\Users\test.gdb"
feature = "feature"  # insert the feature class

def findDuplicates(feature):
    """Calculate the Duplicated features per Instance_S"""
    lista = []
    field = ["OID", "DUPLICATES"]  # change with your field with duplicates
    arcpy.AddField_management(feature, "DUPLICATES", "SHORT")
    print "Field {0} has been added to the {1}".format(field[1], os.path.basename(feature))

    with arcpy.da.SearchCursor(feature, field) as search:
        for row in search:
            id = row[0]
            lista.append(id)

    if field[1] not in [f.name for f in arcpy.ListFields(feature)]:
        print "'{0}' not found in \"{1}\"".format(field[1], os.path.basename(feature))
        print 'Please verify that field names match in "{}"'.format(os.path.basename(feature))
        sys.exit()
    else:
        with arcpy.da.UpdateCursor(feature, field) as cursor:
            for row in cursor:
                id = row[0]
                duplicates = lista.count(id)
                row[1] = duplicates
                cursor.updateRow(row)
        print "Field {0} has been updated in {1}!".format(field[1], os.path.basename(feature))

findDuplicates(feature)
