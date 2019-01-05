# -*- coding: utf-8 -*-
import arcpy
import os
import shutil

# print("The nearest neighbor index is: " + nn_output[0])
# print("The z-score of the nearest neighbor index is: " + nn_output[1])
# print("The p-value of the nearest neighbor index is: " + nn_output[2])
# print("The expected mean distance is: " + nn_output[3])
# print("The observed mean distance is: " + nn_output[4])
# print("The path of the HTML report: " + nn_output[5])

workPath = r"C:\Users\chenpipy\Desktop\xian"
try:
    # Set the current workspace (to avoid having to specify the full path to the feature classes each time)
    arcpy.env.workspace = workPath
    files=arcpy.ListFeatureClasses()
    for file in files:
        try:
            nn_output = arcpy.AverageNearestNeighbor_stats(file, "EUCLIDEAN_DISTANCE", "NO_REPORT", "#")
            rows = arcpy.UpdateCursor(file)
            for row in rows:
                row.setValue("ave_dis", nn_output[4])
                row.setValue("exp_dis", nn_output[3])
                row.setValue("index", nn_output[0])
                row.setValue("p", nn_output[2])
                row.setValue("z", nn_output[1])
                rows.updateRow(row)
        except arcpy.ExecuteError:
            print("跳过")
except arcpy.ExecuteError:
    # If an error occurred when running the tool, print out the error message.
    print(arcpy.GetMessages())
