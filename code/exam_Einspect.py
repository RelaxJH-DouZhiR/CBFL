'''
Author: jhc
Date: 2021-06-15 16:04:17
LastEditTime: 2021-07-12 23:01:24
Description: 用于计算Exam和Einspect@n
'''
from copy import deepcopy
import csv
import json
import linecache
import math
import os
import threading

FATHER_PATH = '/Users/lvlaxjh/code/'  # CBFL文件的父路径
FATHER_PATH2 = "E:/"  # 存储d4j代码以及频谱文件的父路径


# 获取原文件EXAM-start
def get_source_EXAM(project, version):
    CSV_PATH = f"{FATHER_PATH}CBFL/dataset/allPredictResult/{project}/{project}-{version}.csv"
    EXAM_line = 1
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        csvFile = deepcopy(list(csvFile))
        for row in csvFile:
            if row[0] != "project_path" and str(row[5]) != "1":
                EXAM_line += 1
            if str(row[5]) == "1":
                break
    if len(list(csvFile)) == 0 or (EXAM_line) > (len(list(csvFile))-1):
        return 0
    else:
        return (EXAM_line)/(len(list(csvFile))-1)
# 获取原文件EXAM-end


# 获取文件新EXAM-start
def get_new_EXAM(project, version, source_EXAM):
    CSV_PATH = f"{FATHER_PATH}CBFL/dataset/allPredictResult/{project}/{project}-{version}.csv"
    EXAM_line = 1
    predicrtList = []
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        csvFile = deepcopy(list(csvFile))
        for row in csvFile:
            if row[0] != "project_path":
                if str(row[6]) != '-1':
                    newRow = deepcopy(row)
                    if newRow[6] == '1':
                        newRow[6] = 1
                    else:
                        newRow[6] = 0
                    predicrtList.append(deepcopy(newRow))
    # 排序
    predicrtList.sort(key=lambda x: x[6], reverse=True)
    for row in predicrtList:
        if str(row[5]) == str(row[6]) and str(row[5]) == '1':
            break
        else:
            EXAM_line += 1
    if EXAM_line >= len(predicrtList):
        return source_EXAM
    else:
        return (EXAM_line)/(len(list(csvFile))-1)
# 获取原文件新EXAM-end


# 获取原文件Einspect-start
def get_source_Einspect(project, version, step):
    CSV_PATH = f"{FATHER_PATH}CBFL/dataset/allPredictResult/{project}/{project}-{version}.csv"
    inspectList = []
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        csvFile = deepcopy(list(csvFile))
        for row in csvFile:
            if row[0] != "project_path":
                if len(csvFile) > step:
                    if len(inspectList) < step:
                        inspectList.append(deepcopy(row))
                    else:
                        break
                else:
                    inspectList.append(deepcopy(row))
    inspectTotal = 0
    for row in inspectList:
        if str(row[5]) == '1':
            inspectTotal += 1
    return inspectTotal
# 获取原文件Einspect-end


# 获取原文件新Einspect-start
def get_new_Einspect(project, version, step):
    CSV_PATH = f"{FATHER_PATH}CBFL/dataset/allPredictResult/{project}/{project}-{version}.csv"
    inspectList = []
    predicrtList = []  # 预测列表
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        csvFile = deepcopy(list(csvFile))
        for row in csvFile:
            if row[0] != "project_path":
                newRow = deepcopy(row)
                if newRow[6] == '1':
                    newRow[6] = 1
                elif newRow[6] == '0':
                    newRow[6] = 0
                else:
                    newRow[6] = -1
                if newRow[5] == '1':
                    newRow[5] = 1
                else:
                    newRow[5] = 0
                if len(csvFile) > step:
                    if str(row[6]) != '-1':
                        predicrtList.append(deepcopy(newRow))
                    elif str(row[6]) == '-1' and len(predicrtList) < step:
                        predicrtList.append(deepcopy(newRow))
                    else:
                        break
                else:
                    predicrtList.append(deepcopy(newRow))
    inspectTotal = 0
    # 排序
    # predicrtList.sort(key=lambda x: x[5], reverse=True)
    predicrtList.sort(key=lambda x: x[6], reverse=True)
    # predicrtList.sort(key=lambda x: x[5], reverse=True)
    inspectList = predicrtList[:step]
    for row in inspectList:
        if str(row[5]) == '1' and str(row[6]) == '1':
            inspectTotal += 1
    return inspectTotal
# 获取原文件新Einspect-end


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
    classificationFunc = setting["targetTiedK"]["classificationFunc"]
    sampling = setting["targetTiedK"]["sampling"]
    tiedK = setting["targetTiedK"]["tiedK"]
    k = setting["targetTiedK"]["k"]
    EinspectList = setting["@n"]
    # for k_Id in range(k):
    # RESULT_PATH = f"{FATHER_PATH}CBFL/dataset/allPredictResult/result-{project}-{tiedK}-{k}-{k_Id}.csv"
    # allPredictionsResultList += get_all_predictions(RESULT_PATH, project, tiedK, k, k_Id)
    source_EXAM_RES = 0
    new_EXAM_RES = 0
    EinspectList_source_RES = []
    EinspectList_new_RES = []
    for Einspect in EinspectList:
        EinspectList_source_RES.append(0)
        EinspectList_new_RES.append(0)
    for version in versionList:
        source_EXAM = get_source_EXAM(project, version)
        source_EXAM_RES += source_EXAM
        print(f"\033[1;36m get_source_EXAM >{project}< >{version}< >{source_EXAM}< \033[0m")
        new_EXAM = get_new_EXAM(project, version, source_EXAM)
        new_EXAM_RES += new_EXAM
        print(f"\033[1;36m    get_new_EXAM >{project}< >{version}< >{new_EXAM}< \033[0m")
    Einspect_TEM = 0
    for Einspect in EinspectList:
        for version in versionList:
            EinspectList_source_RES[Einspect_TEM] += get_source_Einspect(project, version, Einspect)
            print(f"\033[1;36m EinspectList_source_RES >{project}< >{version}< >{Einspect}< \033[0m")
            EinspectList_new_RES[Einspect_TEM] += get_new_Einspect(project, version, Einspect)
            print(f"\033[1;36m    EinspectList_new_RES >{project}< >{version}< >{Einspect}< \033[0m")
        Einspect_TEM += 1
    print(source_EXAM_RES/len(versionList))
    print(new_EXAM_RES/len(versionList))
    print(EinspectList_source_RES)
    print(EinspectList_new_RES)
    # threadMath = threading.Thread(target=save_predictions, args=(project, version, allPredictionsResultList))
    # threadMath.start()
    # save_predictions(project, version, allPredictionsResultList)
