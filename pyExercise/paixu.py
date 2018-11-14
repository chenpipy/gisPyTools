# -*- coding: utf-8 -*-
import arcpy
import os

filePath = r"C:\Users\chenpipy\Desktop\test\Export_Output.shp"
# Set local variables
fieldName = "TMC"
expression = "accumulate(1)"
codeblock = """total=0
def accumulate(increment):
    global total
    if total:
        total+=increment
    else:
        total=1
    return total"""
# Execute AddField
# arcpy.AddField_management(inTable, fieldName, "SHORT")
# Execute CalculateField
arcpy.CalculateField_management(filePath, fieldName, expression, "PYTHON_9.3",codeblock)
print("完成")
