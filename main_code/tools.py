'''
Author: your name
Date: 2021-06-16 20:05:13
LastEditTime: 2021-06-16 20:23:23
Description: file content
'''
import openpyxl
import json
FATHER_PATH = '/Users/lvlaxjh/code/'

project = 'closure'  # *
settingJson = open('/Users/lvlaxjh/code/CBFL/main_code/setting.json', 'r')
settingContent = settingJson.read()
setting = json.loads(settingContent)
k = setting[project]['k']
versionStart = setting[project]['versionStart']  # 开始版本
versionEnd = setting[project]['versionEnd']  # 最后版本
removeVersionList = setting[project]['removeVersionList']  # 不包含的版本
percentageList = setting['percentageList']  # 前百分比数据列表
topPercentageList = []  # 前百分比数据列表数据
# 计算版本列表-start
versionList = []  # 版本列表
for i in range(versionStart, versionEnd+1):
    if i not in removeVersionList:
        versionList.append(i)
    # 计算版本列表-end

project_all_line = 0
for version in versionList:
    EXCEL_PATH = f'{FATHER_PATH}CBFL/data/{project}/{project}-{version}.xlsx'
    excel = openpyxl.load_workbook(EXCEL_PATH)  # excel文件
    sheet = excel.worksheets[0]  # 表
    line = 2  # sheet 行
    falut_sum = 0  # 错误总数
    print(version)
    while True:
        if sheet.cell(line, 1).value != None:
            line += 1
            project_all_line+=1
        else:
            break
print(project_all_line)
