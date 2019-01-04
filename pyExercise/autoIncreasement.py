# -*- coding: utf-8 -*-
from dirUtil import listDirUtil
# arcgis给选中的要素设置自增，从total开始，自增长的值为increment
total=0
def accumulate(increment):
    global total
    if total:
        total+=increment
    else:
        total=1
    return total
workPath=r"C:\Users\chenpipy\Desktop\青海省"
files=listDirUtil.listAllFiles(workPath.decode("utf-8").encode("gbk"),".shp")
for file in files:
    print(file)
print(len(files))