#coding=utf-8
import arcpy
import os
import shutil
# Create update cursor for feature class
path=r"C:\Users\chenpipy\Desktop\taobao\dem\result"
path1=os.path.join(path,"points")
print(path1)
def createFolder(path):
    if os.path.exists(path):
        print("存在")
        shutil.rmtree(path)
        os.makedirs(path)
        print("删除并创建成功")
    else:
        os.makedirs(path)
        print("创建成功")
createFolder(path1)
print("完成")
