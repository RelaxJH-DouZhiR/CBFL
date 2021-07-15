'''
Author: jhc
Date: 2021-06-15 16:04:17
LastEditTime: 2021-07-08 02:10:00
Description: 获取并写会预测数据
'''
from copy import deepcopy
import csv
import json
import linecache
import math
import os
import threading


FATHER_PATH = "C:/ssdcode/"  # CBFL文件的父路径
FATHER_PATH2 = "E:/"  # 存储d4j代码以及频谱文件的父路径


def get_all_predictions(RESULT_PATH, project, percentage, kFold, k):
    resultList = []
    with open(RESULT_PATH) as f:
        csvFile = csv.reader(f)
        for row in csvFile:
            if row[0] != "dataset":
                resultList.append(deepcopy(row))
    return resultList


def save_predictions(project, version, allPredictionsResultList):
    CSV_PATH = f"{FATHER_PATH}CBFL/dataset/allPredictResult/{project}/{project}-{version}.csv"
    MERGE_CSV_PATH = f"{FATHER_PATH}CBFL/dataset/{project}/{project}-{version}.csv"
    resultList = []
    with open(MERGE_CSV_PATH) as f:
        csvFile = csv.reader(f)
        csvFile = deepcopy(list(csvFile))
        for row in csvFile:
            if row[0] != "project_path":
                newRow = deepcopy(row)
                isPredicted = False
                predictions = "-2"
                for testRow in allPredictionsResultList:
                    if row[0] == testRow[2] and row[1] == testRow[3] and row[2] == testRow[4]:
                        isPredicted = True
                        predictions = testRow[21]
                        break
                if isPredicted:
                    newRow[6] = predictions
                else:
                    newRow[6] = "-1"
                isPredicted = False
                predictions = 0
                resultList.append(deepcopy(newRow))
    targetSaveCSVFile = open(CSV_PATH, "w", encoding="utf-8", newline="")
    targetCSVWriter = csv.writer(targetSaveCSVFile)
    targetCSVWriter.writerow(["project_path", "version", "lines", "statement", "suspicious", "faulty", "predict", "miss_line"])
    for row in resultList:
        targetCSVWriter.writerow(row)
    targetSaveCSVFile.close()
    print(f"\033[1;36m save_predictions >{project}< >{version}< \033[0m")


if __name__ == "__main__":
    project = "mockito"  # chart lang math time mockito closure 项目
    settingJson = open(f"{FATHER_PATH}CBFL/code/setting.json", "r", encoding="utf-8")
    settingContent = settingJson.read()
    setting = json.loads(settingContent)
    versionStart = setting[project]["versionStart"]  # 开始版本
    versionEnd = setting[project]["versionEnd"]  # 结束版本
    removeVersionList = setting[project]["removeVersionList"]  # 不包含的版本
    # 计算版本列表-start
    versionList = []  # 版本列表
    for i in range(versionStart, versionEnd + 1):
        if i not in removeVersionList:
            versionList.append(i)
    settingJson = open(f"{FATHER_PATH}CBFL/code/setting.json", "r", encoding="utf-8")
    settingContent = settingJson.read()
    setting = json.loads(settingContent)
    #
    classificationFunc = setting["targetPercentage"]["classificationFunc"]
    sampling = setting["targetPercentage"]["sampling"]
    percentage = setting["targetPercentage"]["percentage"]
    k = setting["targetPercentage"]["k"]
    allPredictionsResultList = []
    for k_Id in range(k):
        RESULT_PATH = f"{FATHER_PATH}CBFL/dataset/allPredictResult/result-{project}-{percentage}-{k}-{k_Id}.csv"
        allPredictionsResultList += get_all_predictions(RESULT_PATH, project, percentage, k, k_Id)
    for version in versionList:
    # for version in [10]:
        threadMath = threading.Thread(target=save_predictions, args=(project, version, allPredictionsResultList))
        threadMath.start()
        # save_predictions(project, version, allPredictionsResultList)
