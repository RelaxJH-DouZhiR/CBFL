'''
Author: your name
Date: 2021-05-18 09:51:21
LastEditTime: 2021-05-18 10:17:52
Description: file content
'''
import linecache
import openpyxl
CODE_FILE_PATH = '/Users/lvlaxjh/code/CBFL/AST/EclipseAST/App.java'
EXCEL_FILE_PATH = '/Users/lvlaxjh/code/CBFL/FileProcessing/123.xlsx'
excel = openpyxl.load_workbook(EXCEL_FILE_PATH)#excel文件
sheet = excel.worksheets[0]#表
line = 2#sheet 行
codeLineList = []#存储代码行
#读sheet-start
while True:
    if sheet.cell(line, 2).value != None:
        codeLineList.append(sheet.cell(line, 2).value)
    else:
        break
    line+=1
line = 2
#读sheet-end
#读代码，写sheet-start
for i in codeLineList:
    the_line = linecache.getline(CODE_FILE_PATH, i)
    # print(the_line)
    sheet.cell(line, 3).value = the_line
    line +=1
#读代码，写sheet-end
excel.save(EXCEL_FILE_PATH)#存储文件

