# -*- coding: utf-8 -*-
import arcpy
import os

#这个主要是遍历文件夹下面所有的
workPath = r"C:\Users\chenpipy\Desktop\qinghai"
dropFields = ["pinyin"]
for dirpath,dirnames,filenames in os.walk(workPath):
    for file in filenames:
        filePath=os.path.join(dirpath, file).decode('gbk')
        extension=os.path.splitext(file)[1]
        if(extension==".shp"):
            arcpy.DeleteField_management(filePath.encode('utf-8'), dropFields)
            print (filePath.encode('utf-8')+"删除完成")

print("全部完成")
