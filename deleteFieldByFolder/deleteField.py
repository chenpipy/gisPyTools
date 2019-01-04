# -*- coding: utf-8 -*-
import arcpy
import os
from dirUtil import listDirUtil

#这个主要是遍历文件夹下面所有的文件
workPath = r"C:\Users\chenpipy\Desktop\青海省"
dropFields = ["pinyin"]
expression="qq656101529"
# 后续整理成方法
# 删除字段 arcpy.DeleteField_management(filePath.encode('utf-8'), dropFields)
# 添加字段 arcpy.AddField_management(filePath, "url", "TEXT", field_length=50)
#文件夹所有图层添加字段并赋值属性,对使用双引号的字符串添加单引号（'"字符串"'）。
filePaths=listDirUtil.listAllFiles(workPath.decode("utf-8").encode("gbk"),".shp")
for filePath in filePaths:
    arcpy.CalculateField_management(filePath, "url", '"qq656101529"', "PYTHON_9.3")
    print(filePath+u"字段赋值完成")
