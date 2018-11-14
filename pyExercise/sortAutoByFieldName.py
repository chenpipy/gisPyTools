# -*- coding: utf-8 -*-
import arcpy
import os

workPath = r"C:\Users\chenpipy\Desktop\qinghai"
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


def listFirseDir(workPath):
    for filename in os.listdir(workPath):
        filepath = os.path.join(workPath, filename).decode('gbk')
        if os.path.isfile(filepath):
            extension = os.path.splitext(filepath)[1]
            if (extension == ".shp"):
                arcpy.CalculateField_management(filepath, fieldName, expression, "PYTHON_9.3", codeblock)
                print(filepath)

listFirseDir(workPath)
