#此版本为去掉注释版本

# -*- coding: utf-8 -*-
import arcpy
import os
import shutil

# in_feature = r"C:\Users\chenpipy\Desktop\taobao\dem\result\source\source.shp"
# workPath = r"C:\Users\chenpipy\Desktop\taobao\dem\result"

in_feature=arcpy.GetParameterAsText(0)
fieldName=arcpy.GetParameterAsText(1)
workPath=arcpy.GetParameterAsText(2)
fileName=arcpy.GetParameterAsText(3)

outSplitPath = os.path.join(workPath, "split")
outPointsPath = os.path.join(workPath, "points")
outResultPath = os.path.join(workPath, "result")


def createFolder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs(path)
    else:
        os.makedirs(path)
        print("sucess")
try:
    createFolder(outSplitPath)
    createFolder(outPointsPath)
    createFolder(outResultPath)
    arcpy.env.workspace = outSplitPath
    arcpy.Split_analysis(in_feature, in_feature, fieldName, outSplitPath)


    featureclasses = arcpy.ListFeatureClasses()
    for featureclass in featureclasses:
        # 为每个面加上四至范围坐标和XY坐标
        arcpy.AddField_management(in_feature, "x", "DOUBLE")
        arcpy.AddField_management(in_feature, "y", "DOUBLE")
        arcpy.AddField_management(in_feature, "dir", "TEXT")
        name = featureclass.split(".shp")
        outFeaturePoint = outPointsPath + "\\" + name[0] + ".shp"
        arcpy.FeatureVerticesToPoints_management(featureclass, outFeaturePoint, "ALL")
    arcpy.env.workspace = outPointsPath
    points = arcpy.ListFeatureClasses()
    for point in points:
        rows = arcpy.UpdateCursor(point)
        for row in rows:
            if row.getValue("FID") == 0:
                rows.deleteRow(row)
                print("delete first row")
                break
        arcpy.CalculateField_management(point, "x", "!shape.extent.xmin!", "PYTHON_9.3")
        arcpy.CalculateField_management(point, "y", "!shape.extent.ymin!", "PYTHON_9.3")
        extent = arcpy.Describe(point).extent
        xmin = extent.XMin
        xmax = extent.XMax
        ymin = extent.YMin
        ymax = extent.YMax
        name = point.split(".shp")
        outFeaturePoint = outResultPath + "\\" + name[0] + ".shp"
        where_clause = '"x" = ' + str(xmin) + ' or ' + '"x" = ' + str(xmax) + ' or ' + '"y" = ' + str(
            ymin) + ' or ' + '"y" = ' + str(ymax)
        arcpy.Select_analysis(point, outFeaturePoint, where_clause)
    arcpy.env.workspace = outResultPath
    resultPoints = arcpy.ListFeatureClasses()

    for resultPoint in resultPoints:
        rows = arcpy.UpdateCursor(resultPoint)
        extent = arcpy.Describe(resultPoint).extent
        xmin = extent.XMin
        xmax = extent.XMax
        ymin = extent.YMin
        ymax = extent.YMax
        for row in rows:
            x = row.getValue("x")
            y = row.getValue("y")
            if str(x) == str(xmin):
                row.setValue("dir", "3")
            elif str(x) == str(xmax):
                row.setValue("dir", "1")
            elif str(y) == str(ymin):
                row.setValue("dir", "2")
            elif str(y) == str(ymax):
                row.setValue("dir", "4")
            rows.updateRow(row)

    resultshp = workPath + "\\" + fileName+".shp"
    arcpy.Merge_management(resultPoints, resultshp)
    shutil.rmtree(outSplitPath)
    shutil.rmtree(outPointsPath)
    print("done!")
except arcpy.ExecuteError:
    print arcpy.GetMessages()
