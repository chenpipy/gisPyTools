# 获取面的四至点（最东南西北四个点）
# -*- coding: utf-8 -*-
import arcpy
import os
import shutil

# in_feature = r"C:\Users\chenpipy\Desktop\taobao\dem\result\source\source.shp"
# workPath = r"C:\Users\chenpipy\Desktop\taobao\dem\result"

#数据类型：要素类
in_feature=arcpy.GetParameterAsText(0)
#数据类型：字段（关联要素类）
fieldName=arcpy.GetParameterAsText(1)
#数据类型：文件夹
workPath=arcpy.GetParameterAsText(2)
#数据类型：字符串
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


# def deleteAll(path):
#     for i in os.listdir(path):
#         path_file=os.path.join(path,i)
#         if os.path.isfile(path_file):
#             os.remove(path_file)
#     print("清空文件夹成功")


try:
    createFolder(outSplitPath)
    createFolder(outPointsPath)
    createFolder(outResultPath)
    arcpy.env.workspace = outSplitPath
    # 1、分割导入的面（如果存在面压盖的情况，会有问题）
    arcpy.Split_analysis(in_feature, in_feature, fieldName, outSplitPath)

    #如果有重叠的面，用这个方法分割
    # cursor = arcpy.SearchCursor(in_feature)
    # for row in cursor:
    #     name = row.getValue(fieldName)
    #     arcpy.AddMessage(name)
    #     outFeaturePoint = outSplitPath + "\\" + name + ".shp"
    #     where_clause = '"' + fieldName + '"' + '=' + '\'' + name + '\''
    #     arcpy.AddMessage("splitFeature" + name)
    #     arcpy.Select_analysis(in_feature, outFeaturePoint, where_clause)

    # 2、遍历分割的面，每个面导出成折点数据

    featureclasses = arcpy.ListFeatureClasses()
    for featureclass in featureclasses:
        # 为每个面加上四至范围坐标和XY坐标
        arcpy.AddField_management(featureclass, "x", "DOUBLE")
        arcpy.AddField_management(featureclass, "y", "DOUBLE")
        arcpy.AddField_management(featureclass, "dir", "TEXT")
        name = featureclass.split(".shp")
        outFeaturePoint = outPointsPath + "\\" + name[0] + ".shp"
        arcpy.FeatureVerticesToPoints_management(featureclass, outFeaturePoint, "ALL")

    # 3、为所有的折点设置XY坐标值
    # 重新设置环境变量
    arcpy.env.workspace = outPointsPath
    points = arcpy.ListFeatureClasses()
    for point in points:
        rows = arcpy.UpdateCursor(point)
        # 删除第一行（重复的bug）
        for row in rows:
            if row.getValue("FID") == 0:
                rows.deleteRow(row)
                print("delete first row")
                break
        # 字段计算
        arcpy.CalculateField_management(point, "x", "!shape.extent.xmin!", "PYTHON_9.3")
        arcpy.CalculateField_management(point, "y", "!shape.extent.ymin!", "PYTHON_9.3")
        # 获取四至范围
        extent = arcpy.Describe(point).extent
        xmin = extent.XMin
        xmax = extent.XMax
        ymin = extent.YMin
        ymax = extent.YMax
        # Set local variables
        name = point.split(".shp")
        outFeaturePoint = outResultPath + "\\" + name[0] + ".shp"
        where_clause = '"x" = ' + str(xmin) + ' or ' + '"x" = ' + str(xmax) + ' or ' + '"y" = ' + str(
            ymin) + ' or ' + '"y" = ' + str(ymax)
        # Execute Select
        arcpy.Select_analysis(point, outFeaturePoint, where_clause)
    # 4、设置每个点的方向
    # 重新设置环境变量
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
    # 5、合并要素点文件
    resultshp = workPath + "\\" + fileName + ".shp"
    arcpy.Merge_management(resultPoints,resultshp)
    shutil.rmtree(outSplitPath)
    shutil.rmtree(outPointsPath)
    print("done!")
except arcpy.ExecuteError:
    print arcpy.GetMessages()
