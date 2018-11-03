'''
 Name: 根据矢量分割结果，裁剪栅格数据
 Description: Converts features to a raster dataset.
'''
# -*- coding: utf-8 -*-
import arcpy
from arcpy import env
import os
import string
try:

    # Import system modules
    import arcpy
    from arcpy import env
    # Set environment settings
    # workPath=r"C:\Users\toroot\Desktop\myfolder\temp\study\study.gdb"
    workPath=arcpy.GetParameterAsText(0)
    field=arcpy.GetParameterAsText(1)
    cellSize=arcpy.GetParameterAsText(2)
    outPath=arcpy.GetParameterAsText(3)
    env.workspace = workPath
    # Set local variables
    # outPath = r"C:\Users\toroot\Desktop\myfolder\test\result"
    cellSize = 5
    # field = "score"
    type=".tif"
    features=arcpy.ListFeatureClasses()
    for feature in features:
        #splitext 分割成文件名和扩展名的数组(在脚本工具中添加参数不可用)
        #name=os.path.splitext(feature)[0]
        name=feature.split(".shp")
        outRaster=outPath+"\\"+name[0]+type
        arcpy.AddMessage(outRaster)
        # print(outRaster)
        # Execute FeatureToRaster
        arcpy.FeatureToRaster_conversion(feature, field, outRaster, cellSize)
except arcpy.ExecuteError:
    print arcpy.GetMessages()
