'''
Author: jhc
Date: 2021-06-15 16:04:17
LastEditTime: 2021-07-13 14:19:24
Description: 用于前百分比数据，并生成交叉验证数据集
'''
"""
███████╗ ██████╗██████╗ ██╗██████╗ ████████╗    ██████╗ ███████╗██████╗  ██████╗███████╗███╗   ██╗████████╗ █████╗  ██████╗ ███████╗
██╔════╝██╔════╝██╔══██╗██║██╔══██╗╚══██╔══╝    ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝████╗  ██║╚══██╔══╝██╔══██╗██╔════╝ ██╔════╝
███████╗██║     ██████╔╝██║██████╔╝   ██║       ██████╔╝█████╗  ██████╔╝██║     █████╗  ██╔██╗ ██║   ██║   ███████║██║  ███╗█████╗
╚════██║██║     ██╔══██╗██║██╔═══╝    ██║       ██╔═══╝ ██╔══╝  ██╔══██╗██║     ██╔══╝  ██║╚██╗██║   ██║   ██╔══██║██║   ██║██╔══╝
███████║╚██████╗██║  ██║██║██║        ██║       ██║     ███████╗██║  ██║╚██████╗███████╗██║ ╚████║   ██║   ██║  ██║╚██████╔╝███████╗
╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝        ╚═╝       ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
"""
import copy
import csv
import json
import linecache
import math
import os
import threading
from copy import deepcopy
import openpyxl
from analytic_complexity import save_as_csv


FATHER_PATH = "C:/ssdcode/"  # CBFL文件的父路径
FATHER_PATH2 = "E:/"  # 存储d4j代码以及频谱文件的父路径


# 从频谱中获取可疑度语句并存储-start----------------------------------------------------------------
def get_sus_spectrum(project, version, CODE_FILE_PATH):
    CODE_FILE_PATH = FATHER_PATH2 + CODE_FILE_PATH
    # 目标CSV存储位置
    TARGET_CSV_PATH = f"{FATHER_PATH}CBFL/dataset/{project}/"
    #
    # 包含真实缺陷文件路径
    TRUE_FAULT_FILE_PATH = f"{FATHER_PATH2}D4j/{project.capitalize()}/{version}/gzoltars/{project.capitalize()}/{version}/fault.txt"
    trueFaultFile = open(TRUE_FAULT_FILE_PATH, "r", encoding="utf-8")
    trueFaultFileLineList = trueFaultFile.readlines()
    #
    # 频谱原文件
    SPECTRUM_FILE_PATH = f"{FATHER_PATH2}D4j/{project.capitalize()}/{version}/gzoltars/{project.capitalize()}/{version}/Dstar_{project.capitalize()}_{version}.txt"
    spectrumFile = open(SPECTRUM_FILE_PATH, "r", encoding="utf-8")
    spectrumFileLineList = spectrumFile.readlines()
    #
    # 目标存储csv
    targetCSVFile = open(f"{TARGET_CSV_PATH}{project}-{version}.csv", "w", encoding="utf-8", newline="")
    #
    targetCSVWriter = csv.writer(targetCSVFile)
    # csv文件头
    targetCSVWriter.writerow(["project_path", "version", "lines", "statement", "suspicious", "faulty", "predict", "miss_line"])
    #
    resultList = []  # 结果列表
    resultDict = {
        "project_path": "",
        "version": "",
        "lines": "",
        "statement": "",
        "suspicious": "",
        "faulty": "",
        "predict": "",
        "miss_line": "",
    }  # 结果字典
    for lineNumber in range(len(spectrumFileLineList)):
        spectrumFileLineContentList = spectrumFileLineList[lineNumber].rstrip("\n").split("#")
        # 去除'$'-start
        if "$" in spectrumFileLineContentList[1]:
            spectrumFileLineContentList[1] = spectrumFileLineContentList[1][: spectrumFileLineContentList[1].find("$")]
        resultDict["project_path"] = deepcopy(spectrumFileLineContentList[1].replace(".", "/"))
        resultDict["version"] = deepcopy(version)
        resultDict["lines"] = deepcopy(int(spectrumFileLineContentList[2]))
        # 去除'$'-end
        # 暂时检测文件路径错误---------------------------------------------------------------
        try:
            files = open(CODE_FILE_PATH + resultDict["project_path"] + ".java", "r")
            files.close()
        except Exception as e:
            print(e)
            print(f"\033[1;31m get_sus_spectrum path error {project} {version}\033[0m")
            while True:
                pass
        # 暂时检测文件路径错误---------------------------------------------------------------
        # 获取代码-start
        try:
            lineCode = linecache.getline(CODE_FILE_PATH + resultDict["project_path"] + ".java", resultDict["lines"])
        except Exception:
            files = open(CODE_FILE_PATH + resultDict["project_path"] + ".java", "r", encoding="iso-8859-1")
            codeFileLineList = files.readlines()
            lineCode = codeFileLineList[resultDict["lines"] - 1]
        resultDict["statement"] = deepcopy(str(lineCode).rstrip("\n"))
        resultDict["suspicious"] = deepcopy(float(spectrumFileLineContentList[3]))
        # 获取真实缺陷定位-start
        isFault = False  # 是否为真实缺陷，默认为False
        isMissLine = False  # 是否为确实缺陷定位
        for trueFaultNumber in range(len(trueFaultFileLineList)):
            trueFaultfileLineContentList = trueFaultFileLineList[trueFaultNumber].rstrip("\n").split("#")
            if spectrumFileLineContentList[1] + ".java" == trueFaultfileLineContentList[0] and spectrumFileLineContentList[2] == trueFaultfileLineContentList[1]:
                isFault = True
                isMissLine = False
                print(project + "-" + str(version) + " " + spectrumFileLineContentList[1] + "-" + spectrumFileLineContentList[2] + " -> is true fault")
                del trueFaultFileLineList[trueFaultNumber]
                break
            else:
                isFault = False
            # 插入未定位-start
            if spectrumFileLineContentList[1] + ".java" == trueFaultfileLineContentList[0] and spectrumFileLineContentList[2] >= trueFaultfileLineContentList[1] and "FAULT_OF_OMISSION" in trueFaultfileLineContentList[2]:
                isFault = True
                print(project + "-" + str(version) + " " + spectrumFileLineContentList[1] + "-" + spectrumFileLineContentList[2] + " -> is miss fault")
                isMissLine = True
                del trueFaultFileLineList[trueFaultNumber]
                break
            else:
                isFault = False
            # 插入未定位-end
        if isFault:
            resultDict["faulty"] = 1
        else:
            resultDict["faulty"] = 0
        if isMissLine:
            resultDict["miss_line"] = 1
        else:
            resultDict["miss_line"] = 0
        resultList.append(deepcopy(resultDict))
    for result in resultList:
        targetCSVWriter.writerow([result["project_path"], result["version"], result["lines"], result["statement"], result["suspicious"], result["faulty"], result["predict"], result["miss_line"]])
    targetCSVFile.close()
    print(f"\033[1;36m get_sus_spectrum >{project}< >{version}< \033[0m")


# 获取AST文件列表-start
def save_all_AST_path(project, version, CODE_FILE_PATH):
    # AST文件列表存储
    targetASTPathSaveFile = open(f"{FATHER_PATH}CBFL/dataset/{project}/ASTpath/{project}-{version}.txt", "w", encoding="utf-8")
    with open(f"{FATHER_PATH}CBFL/dataset/{project}/{project}-{version}.csv") as f:
        csvFile = csv.reader(f)
        javaCodeFilePathList = []
        for row in csvFile:
            if row[0] != "project_path":
                javaCodeFilePath = CODE_FILE_PATH + row[0]
                javaCodeFilePathList.append(javaCodeFilePath)
    resultPathList = []
    for i in javaCodeFilePathList:
        if i not in resultPathList:
            resultPathList.append(deepcopy(i))
    del i
    # 检测错误路径
    for i in resultPathList:
        try:
            files = open(FATHER_PATH2 + i + ".java", "r")
            files.close()
        except Exception as e:
            print(e)
            print(f"\033[1;31m save_all_AST_path path error {FATHER_PATH2+i} \033[0m")
            while True:
                pass
    #
    for i in resultPathList:
        targetASTPathSaveFile.write(i)
        targetASTPathSaveFile.write("\n")
    targetASTPathSaveFile.close()
    print(f"\033[1;36m save_all_AST_path >{project}< >{version}< \033[0m")


# 获取文件前百分条数语句-start
def get_top_percent(percentage, project, version):
    with open(f"{FATHER_PATH}CBFL/dataset/{project}/complexity/{project}-{version}.csv") as f:
        csvFile = csv.reader(f)
        csvFile = list(csvFile)
        fileLength = len(csvFile) - 1
        needLineLength = math.ceil(fileLength * (percentage / 100))
        if needLineLength > fileLength:
            needLineLength = fileLength
        csvLine_LOOP = 1  # 记录行数
        resultList = []  # 存储前百分比的结果
        for row in csvFile:
            if row[0] != "dataset":
                if csvLine_LOOP <= needLineLength:
                    rows = row
                    rows.append(-1)
                    resultList.append(deepcopy(rows))
                else:
                    break
                csvLine_LOOP += 1
    return resultList


# 保存文件前百分条数语句-start
def save_top_percent(percentageList, percentage, project):
    # 目标存储csv
    targetSaveCSVFile = open(f"{FATHER_PATH}CBFL/dataset/{project}/percentFile/{project}-{percentage}.csv", "w", encoding="utf-8", newline="")
    #
    targetCSVWriter = csv.writer(targetSaveCSVFile)
    # csv文件头
    targetCSVWriter.writerow(["dataset", "project", "path", "version", "codeLine", "statement", "varTotal", "optTotal", "array", "bracketDepth", "bracketTotal", "keywordTotal", "methodTotal", "typeTotal", "logic", "lengthEle", "lengthWord", "depth", "suspicious", "accuracy", "miss_line", "predict"])
    for result in percentageList:
        targetCSVWriter.writerow(result)
    targetSaveCSVFile.close()
    print(f"\033[1;36m save_top_percent >{project}< >{percentage}< \033[0m")


# 获取项目中所有真实缺陷语句-start
def get_all_fault(project, version):
    with open(f"{FATHER_PATH}CBFL/dataset/{project}/complexity/{project}-{version}.csv") as f:
        csvFile = csv.reader(f)
        resultList = []  # 存储前百分比的结果
        for row in csvFile:
            if row[0] != "dataset" and row[19] == "1":
                resultList.append(deepcopy(row))
    print(f"\033[1;36m get_all_fault >{project}< >{version}< \033[0m")
    return resultList


# 存储项目中所有真实缺陷语句-start
def save_all_fault(resultList, project):
    targetSaveCSVFile = open(f"{FATHER_PATH}CBFL/dataset/{project}/percentFile/{project}-all-fault.csv", "w", encoding="utf-8", newline="")
    targetCSVWriter = csv.writer(targetSaveCSVFile)
    targetCSVWriter.writerow(["dataset", "project", "path", "version", "codeLine", "statement", "varTotal", "optTotal", "array", "bracketDepth", "bracketTotal", "keywordTotal", "methodTotal", "typeTotal", "logic", "lengthEle", "lengthWord", "depth", "suspicious", "accuracy", "miss_line", "predict"])
    for result in resultList:
        result_TEM = deepcopy(result)
        result_TEM.append(-1)
        targetCSVWriter.writerow(result_TEM)
    targetSaveCSVFile.close()
    print(f"\033[1;36m save_all_fault >{project}< \033[0m")


# 生成k折交叉验证数据集-start
def k_fold(project, kFold, percentage):
    PERCENTAGE_CSV_PATH = f"{FATHER_PATH}CBFL/dataset/{project}/percentFile/{project}-{percentage}.csv"  # 百分比文件
    allContentList = []
    with open(PERCENTAGE_CSV_PATH) as f:
        csvFile = csv.reader(f)
        for row in csvFile:
            if row[0] != "dataset":
                allContentList.append(deepcopy(row))
    # 获取项目中全部真实缺陷，用于后续补全训练集-start
    allFaultList = []  # 版本中全部真实缺陷列表
    with open(f"{FATHER_PATH}CBFL/dataset/{project}/percentFile/{project}-all-fault.csv") as f:
        csvFile = csv.reader(f)
        for row in csvFile:
            if row[0] != "dataset":
                allFaultList.append(deepcopy(row))
    # 获取项目中全部真实缺陷，用于后续补全训练集-end
    testDataset_step = math.floor(len(allContentList) / kFold)  # 交叉验证，步长
    testDataset_TEM = 0  # 临时变量，用于后续写个数据集使用
    for k in range(kFold):
        trainDatasetList = []  # 训练集列表
        testDatasetList = []  # 测试集列表
        # 根据步长和切割生成测试集-start
        if k == kFold - 1:  # 为最后一轮
            isFault_add_step_TEM = len(allContentList)
        else:
            isFault_add_step_TEM = testDataset_TEM + testDataset_step
        for row in allContentList[testDataset_TEM:isFault_add_step_TEM]:
            testDatasetList.append(deepcopy(row))  # 真实缺陷
        testDataset_TEM += testDataset_step
        # 根据步长和切割生成测试集-end
        # 训练集-start
        trainDatasetList = deepcopy(allContentList)
        # 训练集-end
        # 将全部真实缺陷插入训练集-start
        for row in allFaultList:
            trainDatasetList.append(row)
        # 将全部真实缺陷插入训练集-end
        # 训练集去重-start
        resultTrainDatasetList_TEM = []
        isDuplicate = False  # 是否重复
        for row in trainDatasetList:
            for testRow in resultTrainDatasetList_TEM:
                if (
                    row[6] == testRow[6]
                    and row[7] == testRow[7]
                    and row[8] == testRow[8]
                    and row[9] == testRow[9]
                    and row[10] == testRow[10]
                    and row[11] == testRow[11]
                    and row[12] == testRow[12]
                    and row[13] == testRow[13]
                    and row[14] == testRow[14]
                    and row[15] == testRow[15]
                    and row[17] == testRow[17]
                ):
                    isDuplicate = True
                    break
            if not isDuplicate:
                resultTrainDatasetList_TEM.append(deepcopy(row))
            isDuplicate = False
        trainDatasetList = deepcopy(resultTrainDatasetList_TEM)
        # 测试集训练集去重-start
        resultTrainDatasetList_TEM = []
        isIntest = False  # 是否重复
        for row in trainDatasetList:
            for testRow in testDatasetList:
                if row[2] == testRow[2] and row[3] == testRow[3] and row[4] == testRow[4]:
                    isIntest = True
                    break
            if not isIntest:
                resultTrainDatasetList_TEM.append(row)
            isIntest = False
        trainDatasetList = deepcopy(resultTrainDatasetList_TEM)
        # 测试集训练集去重-end
        # 训练集去重-end
        testDatasetCsvFile = open(f"{FATHER_PATH}CBFL/dataset/{project}/percentage_traintest/test-{project}-{percentage}-{kFold}-{k}.csv", "w", encoding="utf-8", newline="")
        testCsvWriter = csv.writer(testDatasetCsvFile)
        testCsvWriter.writerow(
            ["dataset", "project", "path", "version", "codeLine", "statement", "varTotal", "optTotal", "array", "bracketDepth", "bracketTotal", "keywordTotal", "methodTotal", "typeTotal", "logic", "lengthEle", "lengthWord", "depth", "suspicious", "accuracy", "miss_line", "predict"]
        )
        for row in testDatasetList:
            testCsvWriter.writerow(row)
        testDatasetCsvFile.close()
        trainDatasetCsvFile = open(f"{FATHER_PATH}CBFL/dataset/{project}/percentage_traintest/train-{project}-{percentage}-{kFold}-{k}.csv", "w", encoding="utf-8", newline="")
        trainCsvWriter = csv.writer(trainDatasetCsvFile)
        trainCsvWriter.writerow(
            ["dataset", "project", "path", "version", "codeLine", "statement", "varTotal", "optTotal", "array", "bracketDepth", "bracketTotal", "keywordTotal", "methodTotal", "typeTotal", "logic", "lengthEle", "lengthWord", "depth", "suspicious", "accuracy", "miss_line", "predict"]
        )
        for row in trainDatasetList:
            trainCsvWriter.writerow(row)
        trainDatasetCsvFile.close()
    print(f"\033[1;36m k_fold >{project}< >{percentage}< >{kFold}<  \033[0m")


if __name__ == "__main__":
    project = "chart"  # chart lang math time mockito closure 项目
    settingJson = open(f"{FATHER_PATH}CBFL/code/setting.json", "r", encoding="utf-8")
    settingContent = settingJson.read()
    setting = json.loads(settingContent)
    versionStart = setting[project]["versionStart"]  # 开始版本
    versionEnd = setting[project]["versionEnd"]  # 结束版本
    removeVersionList = setting[project]["removeVersionList"]  # 不包含的版本
    percentageList = setting["percentageList"]  # 前百分比数据列表
    KList = setting["k"]
    tiedKList = setting["tiedK"]
    # 计算版本列表-start
    versionList = []  # 版本列表
    for i in range(versionStart, versionEnd + 1):
        if i not in removeVersionList:
            versionList.append(i)
    # 计算版本列表-end
    # ------------------------------------------------------------------------------
    # for version in versionList:
    #     javaCodeFilePath = f"DSatr/{project}-direct/{project}-{version}/" + setting[project]["javaCodeFilePath"]
    #     if (project == "lang" and version >= 36) or (project == "math" and version >= 85):
    #         javaCodeFilePath = f"DSatr/{project}-direct/{project}-{version}/" + setting[project]["javaCodeFilePath2"]
    #
    # get_sus_spectrum(project, version, javaCodeFilePath)
    #
    # save_all_AST_path(project, version, javaCodeFilePath)
    # 多线程
        # threadMath = threading.Thread(target=save_as_csv, args=(f"{FATHER_PATH}CBFL/dataset/{project}/{project}-{version}.csv", f"{FATHER_PATH}CBFL/dataset/{project}/complexity/", FATHER_PATH2 + javaCodeFilePath, version, project))
        # threadMath.start()
    # ------------------------------------------------------------------------------
    # 存储项目中全部真实缺陷-start----------------------------------------------------------------
    allFaultList = []
    for version in versionList:
        allFaultList += get_all_fault(project, version)
    save_all_fault(allFaultList, project)
    del allFaultList
    # 存储项目中全部真实缺陷-end------------------------------------------------------------------
    # 取百分比文件并生成k折交叉训练集-start--------------------------------------------------------
    percentageContentSaveList = []
    for percentage in percentageList:
        # 取百分比----------------------------------
        for version in versionList:
            percentageContentSaveList += get_top_percent(percentage, project, version)
        save_top_percent(percentageContentSaveList, percentage, project)
        percentageContentSaveList = []
        # ----------------------------------
    # for percentage in percentageList:
    #     for k in KList:
    #         k_fold(project, k, percentage)
    # ----------------------------------
    # 取百分比文件并生成k折交叉训练集-end----------------------------------------------------------
