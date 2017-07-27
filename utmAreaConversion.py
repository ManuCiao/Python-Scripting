def utmConversion(feature):
    """Calculate the Area of Polygons reprojecting per UTM Zones using Cursors -- fast performance"""
    utmNorthZone = 32599
    utmSouthZone = 32699
    # note I've changed SHAPE@AREA to SHAPE@ because I want a Geometry object
    # to project and then return the area of rather than a double.
    field = ["SHAPE@", "BASIN_AREA_SQKM", "UTM_ZONES", "NTH_STH"]

    print "Adding Field BASIN_AREA_SQKM to the {}".format(feature)
    arcpy.AddField_management(feature, "BASIN_AREA_SQKM", "DOUBLE")

    if field[1] not in [f.name for f in arcpy.ListFields(feature)]:
        print "'{0}', '{1}' not found in \"{2}\"".format(field[1], feature)
        print 'Please verify that field name matches in "{}"'.format(feature)
        sys.exit()
    else:
        with arcpy.da.UpdateCursor(feature, field) as UCur:
            for URow in UCur:
                Geom = URow[0]
                UTMZone = URow[2]
                Hemi = URow[3].upper()
                UTMZone += 1

                if UTMZone > 0 and UTMZone < 62:
                    # only calculate and update where the zone is in the expected range
                    if Hemi == 'N':
                        OutSR = arcpy.SpatialReference(utmNorthZone + UTMZone)
                        # print "UTM Coordinate System: {}".format(OutSR.name)
                    elif Hemi == 'S':
                        OutSR = arcpy.SpatialReference(utmSouthZone + UTMZone)
                        # print "UTM Coordinate System: {}".format(OutSR.name)
                    else:
                        OutSR = None

                    if OutSR != None:
                        # print "Pick up the UTM Coordinate System as Coord System Env: {}".format(OutSR.name)
                        arcpy.env.outputCoordinateSystem = OutSR
                        proj = Geom.projectAs(OutSR)
                        AreaSqKm = proj.area / (10 ** 6)  # turn square metres into square kilometres.
                        URow[1] = AreaSqKm
                        UCur.updateRow(URow)
        print "Field {0} has been updated to {1}.".format(field[1], feature)

if __init__ = __main__:
  feature = # add the feature class or shp 
  utmConversion(feature)

