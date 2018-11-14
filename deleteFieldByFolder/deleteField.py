# -*- coding: utf-8 -*-
import arcpy
import os

#这个主要是遍历文件夹下面所有的文件
workPath = r"C:\Users\chenpipy\Desktop\qinghai"
dropFields = ["pinyin"]
# 后续整理成方法
def listAllFiles(workPath):
    for dirpath,dirnames,filenames in os.walk(workPath):
        for file in filenames:
            filePath=os.path.join(dirpath, file).decode('gbk')
            extension=os.path.splitext(file)[1]
            if(extension==".shp"):
                arcpy.DeleteField_management(filePath.encode('utf-8'), dropFields)
                print (filePath.encode('utf-8')+"删除完成")
    print("全部完成")


#遍历第一层文件夹（后续整理成方法）

def listFirseDir(workPath):
    for filename in os.listdir(workPath):
        filepath = os.path.join(workPath, filename)
        if os.path.isfile(filepath):
            extension = os.path.splitext(filepath)[1]
            if (extension == ".shp"):
                print(filepath)