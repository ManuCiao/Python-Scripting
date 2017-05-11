import arcpy
import os

feature = "feature" # insert feature class 

def calculateVertexCount(feature):
    """add the Count of Vertexes field to the feature class"""
    # calculate number of vertexes
    field = ["VERTEX_COUNT", "SHAPE@"]
    arcpy.AddField_management(feature, "VERTEX_COUNT", "LONG")
    print "Field {0} has been added to the {1}".format(field[0], os.path.basename(feature))
    if field[0] not in [f.name for f in arcpy.ListFields(feature)]:
        print "'{0}' not found in \"{1}\"".format(field[0], os.path.basename(feature))
        print 'Please verify that field names match in "{}"'.format(os.path.basename(feature))
        sys.exit()
    else:
        with arcpy.da.UpdateCursor(feature, field) as cursor:
            for row in cursor:
                # some features in the pvFields don't have a shape
                shape = row[1]
                if shape is not None:
                    row[0] = abs(shape.pointCount - shape.partCount)
                    cursor.updateRow(row)
                elif shape is None:
                    row[0] = 0
                else:
                    print "Cannot calculate the number of vertexes."
                    sys.exit()
            print "Field {0} has been updated in {1}!".format(field[0], os.path.basename(feature))

calculateVertexCount(feature)
