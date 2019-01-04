# -*- coding: utf-8 -*-
import arcpy
import os
from dirUtil import listDirUtil

# 给某一字段，增加自增长的值
workPath = r"C:\Users\chenpipy\Desktop\xian"
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
# 获取所有的shp文件
filePaths=listDirUtil.listFirstDirFiels(workPath,".shp")
# 遍历
for filePath in filePaths:
    arcpy.CalculateField_management(filePath, fieldName, expression, "PYTHON_9.3", codeblock)
    print (filePath+u"完成")

