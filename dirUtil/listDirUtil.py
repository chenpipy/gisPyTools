# -*- coding: utf-8 -*-
import os

# 遍历文件夹下所有的文件，包含子目录，返回所有文件路径组成的列表
# 中文调用示例：files=listDirUtil.listAllFiles(workPath.decode("utf-8").encode("gbk"))
def listAllFiles(workPath,extension):
    filePathList=[]
    for dirpath,dirnames,filenames in os.walk(workPath):
        for file in filenames:
            filePath=os.path.join(dirpath, file).decode('gbk')
            fileExtension = os.path.splitext(filePath)[1]
            if(extension):
                if (fileExtension ==extension):
                    filePathList.append(filePath)
            else:
                filePathList.append(filePath)
    return filePathList

#遍历文件夹下所有的文件，不包含子文件夹，返回所有文件路径组成的列表
def listFirstDirFiels(workPath,extension):
    filePathList = []
    for filename in os.listdir(workPath):
        filePath = os.path.join(workPath, filename).decode('gbk')
        if os.path.isfile(filePath):
            fileExtension = os.path.splitext(filePath)[1]
            if (extension):
                if (fileExtension == extension):
                    filePathList.append(filePath)
            else:
                filePathList.append(filePath)
    return filePathList